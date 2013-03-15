from flask import Flask, render_template, redirect, jsonify, request

import redis
import math

import settings
import replay
import json
from assets.assets import assets_blueprint

app = Flask(__name__)
app.secret_key = 'SECRET'
app.config.from_object(settings)

app.register_blueprint(assets_blueprint)

accelerometer = [ replay.csv_data(filename) for filename in settings.ACCEL_CSV_FILES ]
fsr_data = replay.csv_data(settings.FSR_CSV_FILE)

r = redis.Redis()

@app.route('/')
def index():
  return redirect('/demo')

@app.route('/record_sleep', methods=["POST"])
def record_sleep():
  t = { 'start' : float(request.form['start'])/1000, 'end' : float(request.form['end'])/1000 }
  r.lpush('sleep-times', json.dumps(t))
  return "OK"

@app.route('/demo')
def demo():
  return render_template('demo.html',
      accel_url="/fake_accel",
      fsr_url="/fake_fsr")

@app.route('/live')
def live():
  return render_template('demo.html',
      accel_url="/accel",
      fsr_url="/fsr")

@app.route('/accel/<accel_id>')
def accel(accel_id):
  t = int(request.args.get('t', 1000))
  samples = max(t / settings.ACCEL_UPDATE, 1)
  raw = (json.loads(s)['data'] for s in r.lrange('accel:%s' % accel_id, 0, samples-1))
  mags = [int(math.sqrt(x*x+y*y+z*z)) for x,y,z in raw]
  print mags
  mag = mags[0]
  for m in mags[1:]:
    if abs(m) > abs(mag):
      mag = m
  return jsonify({'data' : mag})

@app.route('/fsr')
def fsr():
  t = int(request.args.get('t', 1000))
  samples = max(t / settings.FSR_UPDATE, 1)
  raw_datas = [json.loads(s)['data'] for s in r.lrange('fsr', 0, samples-1)]
  max_x = len(raw_datas[0][0])
  max_y = len(raw_datas[0])
  min_ = min((min(row) for row in raw_datas[0]))
  max_ = max((max(row) for row in raw_datas[0]))
  data = [
    {
      'x'     : float(x + 0.5) / max_x,
      'y'     : float(y + 0.5) / max_y,
      'value' : int(float(value - min_) / (max_ - min_) * 1023)
    }
    for y, row in enumerate(raw_datas[0])
    for x, value in enumerate(row)
  ]
  return jsonify({ 'data' : data })

@app.route('/fake_accel/<accel_id>')
def fake_accel(accel_id):
  accel_id = int(accel_id)
  measurement = accelerometer[accel_id].next()
  x,y,z = measurement
  return jsonify({'data' : int(math.sqrt(x*x+y*y+z*z))})

@app.route('/fake_fsr')
def fake_fsr():
  raw_data = [ fsr_data.next() for _ in xrange(6) ]
  print raw_data
  max_x = len(raw_data[0])
  max_y = len(raw_data)
  data = [
    {
      'x'     : float(x + 0.5) / max_x,
      'y'     : float(y + 0.5) / max_y,
      'value' : min(max(value, 0), 1023),
    }
    for y, row in enumerate(raw_data)
    for x, value in enumerate(row)
  ]
  return jsonify({ 'data' : data })

if __name__ == '__main__':
  app.run(debug=True)
