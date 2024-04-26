import os

from flask import (Flask, redirect, render_template, request, send_from_directory, url_for)

app = Flask(__name__)

@app.route('/', methods=["GET"])
def index():
   print('Request for index page received')
   if request.headers.getlist("X-Forwarded-For"):
      ipaddr = request.headers.getlist("X-Forwarded-For")[0]
   else:
      ipaddr = request.remote_addr
   return ipaddr, 200

@app.route('/favicon.ico')
def favicon():
   return send_from_directory(os.path.join(app.root_path, 'static'),
          'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/ping", methods=["GET"])
def ping():
    status_code = 200
    return "Ping OK \(^-^)/\n", status_code

if __name__ == '__main__':
   app.run()
