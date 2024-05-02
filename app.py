import os

from flask import (Flask, make_response, redirect, render_template, request, send_from_directory, url_for)
from flask import jsonify
import socket
from datetime import datetime

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/', methods=["GET"])
def index():
    print('Request for index page received')
    if request.headers.getlist("X-Forwarded-For"):
        print('X-Forwarded-For')
        ipaddrraw = request.headers.getlist("X-Forwarded-For")[0]
    else:
        print('remote_addr')
        ipaddrraw = request.remote_addr
    ipaddrraw = ''.join(ipaddrraw.split())

    ipaddrlst = []
    hostnamelst = []
    for ipaddr in ipaddrraw.split(","):
        ipaddrbody = ipaddr.split(":")[0]
        ipaddrlst.append(ipaddrbody)

        try:
            hostnamelst.append(socket.gethostbyaddr(ipaddrbody)[0])
        except:
            hostnamelst.append('n/a')

    status_code = 200
    response = make_response(
            jsonify(
                {
                    'ip':','.join(ipaddrlst), 
                    'hostname':','.join(hostnamelst),
                    'date': str(datetime.now()),
                    'user_agent': str(request.user_agent),
                    }
                ),
                status_code,
            )
    response.headers["Content-Type"] = "application/json"
    return response

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/ping", methods=["GET"])
def ping():
    status_code = 200
    return "Ping OK \(^-^)/\n", status_code
   
if __name__ == '__main__':
    app.json.sort_keys = False
    app.run()
