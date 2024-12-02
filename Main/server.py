from flask import Flask, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
import json
import time, threading

# nothing but a filename
JSON = "lockdata.json"

# -----------------------------------------------------------------

app = Flask(__name__)
#socketio = SocketIO(app)

data = {"message": "no data received yet"}

@app.route('/')
def serve_html():
    return send_from_directory('.', 'index.html')

# working backup without socketIO - delete if you get socketIO working
@app.route('/data', methods = ['GET'])
def get_data():
    with open(JSON, "r") as file:
        data = json.load(file)
    return jsonify(data)

#@socketio.on('connect')
#def on_connect():
    #print("[Flask_SocketIO] Client connected")

# thread to constantly update from json
#def update():
    #while True:
        #with open(JSON, "r") as file:
            #data = json.load(file)
            #data = jsonify(data)
        #socketio.emit('update', data)
        #time.sleep(0.5)

# -----------------------------------------------------------------

if __name__ == '__main__':
    # route to collect JSON data
    # TODO: at https://localhost:3000/api

    # Grafana listens on port 3000
    # to be added later: in Grafana: configure to ignore validation or add certificates to system's trusted certs

    # generate keys with:
    # TODO: openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.keys -out server.crt

    # enable HTTPS with self-signed cert and private keys at your directory location
    app.run(host = '0.0.0.0', port=3000, ssl_context =
    ('../Main/keys/server.crt',
     '../Main/keys/server.key'))