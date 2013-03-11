from flask import Flask, render_template, redirect, jsonify, request

import settings
import replay
from assets.assets import assets_blueprint

app = Flask(__name__)
app.secret_key = 'SECRET'
app.config.from_object(settings)

app.register_blueprint(assets_blueprint)

accelerometer = [ replay.csv_data(filename) for filename in settings.ACCEL_CSV_FILES ]

@app.route('/')
def index():
  return redirect('/demo')

@app.route('/demo')
def demo():
  return render_template('demo.html')

@app.route('/accel/<accel_id>')
def accel(accel_id):
  accel_id = int(accel_id)
  n = int(request.args.get('n', 1))
  data = [ accelerometer[accel_id - 1].next() for _ in xrange(n) ]
  series = [
    { 'name' : 'x', 'data' : [ reading['x'] for reading in data ] },
    { 'name' : 'y', 'data' : [ reading['y'] for reading in data ] },
    { 'name' : 'z', 'data' : [ reading['z'] for reading in data ] },
  ]
  return jsonify({ 'series' : series })

if __name__ == '__main__':
  app.run(debug=True)
