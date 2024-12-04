from flask import Flask, jsonify, send_from_directory, request
import json
import paho.mqtt.client as mqtt
import time, threading
import ssl

# nothing but a filename
JSON = "lockdata.json"

# -----------------------------------------------------------------
# MQTT

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT server. RC "+str(rc))

# -----------------------------------------------------------------
# HTTPS

app = Flask(__name__)

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

@app.route('/trigger', methods=['POST'])
def trigger_event():
    trigger_data = request.json
    if trigger_data.get('status') == 'pressed':
        # publish a REC mqtt message to the keys topic
        client.publish("samardzi/keys", "frontend_rec")
        return jsonify({"message": "frontend mqtt event triggered"})
    elif trigger_data.get('status') == 'reset':
        # publish a RESET mqtt message to the keys topic
        client.publish("samardzi/keys", "frontend_reset")
        return jsonify({"message": "frontend mqtt event triggered"})
    else:
        return jsonify({"error": "ERR"}), 400
# -----------------------------------------------------------------

if __name__ == '__main__':
    # route to collect JSON data
    # TODO: at https://localhost:3000/api

    # Grafana listens on port 3000
    # to be added later: in Grafana: configure to ignore validation or add certificates to system's trusted certs

    # generate keys with:
    # TODO: openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.keys -out server.crt

    # open mqtt before HTTP
    client = mqtt.Client()

    # enable TLS, disable client-side certificates
    client.tls_set(
        tls_version=ssl.PROTOCOL_TLSv1_2
    )

    client.connect(host="broker.hivemq.com", port=8883, keepalive=60)

    # enable HTTPS with self-signed cert and private keys at your directory location
    app.run(host = '0.0.0.0', port=3000, ssl_context =
    ('../Main/keys/server.crt',
     '../Main/keys/server.key'))
