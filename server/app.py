from flask import Flask, render_template, url_for, redirect, g, session, request, make_response

import settings
from assets.assets import assets_blueprint

app = Flask(__name__)
app.secret_key = 'SECRET'
app.config.from_object(settings)

app.register_blueprint(assets_blueprint)

@app.route('/demo')
def demo():
  return render_template('demo.html')

if __name__ == '__main__':
  app.run(debug=True)
