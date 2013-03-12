from flask import Flask, render_template, redirect, jsonify

import settings
import replay
from assets.assets import assets_blueprint

app = Flask(__name__)
app.secret_key = 'SECRET'
app.config.from_object(settings)

app.register_blueprint(assets_blueprint)

accelerometer = [ replay.csv_data(filename) for filename in settings.ACCEL_CSV_FILES ]
fsr_data = replay.csv_data(settings.FSR_CSV_FILE)

@app.route('/')
def index():
  return redirect('/demo')

@app.route('/demo')
def demo():
  return render_template('demo.html')

@app.route('/accel/<accel_id>')
def accel(accel_id):
  accel_id = int(accel_id)
  measurement = accelerometer[accel_id].next()
  return jsonify({
    'x' : measurement[0],
    'y' : measurement[1],
    'z' : measurement[2],
  })

@app.route('/fsr')
def fsr():
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
