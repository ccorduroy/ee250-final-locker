from flask import Flask, jsonify
import json

# specified JSON path,,same as in other files
JSON = "lockdata.json"

app = Flask(__name__)

# route to collect JSON data
# in grafana: https://<yourip>:3000/api/lock
@app.route('/api/lock', methods = ['GET'])

def getdata():
    with open(JSON, "r") as file:
        data = json.load(file)
    return jsonify(data)

if __name__ == '__main__':
    # Grafana listens on port 3000
    # generate key with:
    # openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout server.key -out server.crt
    # in Grafana: configure to ignore validation or add certificates to system's trusted certs

    # enable HTTPS with self-signed cert and private key
    # I have provided keys for testing for now.
    app.run(host = '0.0.0.0', port=3000, ssl_context =
    ('../Main/keys/server.crt',
     '../Main/keys/server.key'
    ))   # ensure nothing else is listening here