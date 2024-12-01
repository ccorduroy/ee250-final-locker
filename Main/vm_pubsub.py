"""EE 250L Lab 04 Starter Code

Run vm_pubsub.py in a separate terminal on your VM."""
from flask import Flask, jsonify
import paho.mqtt.client as mqtt
import time
from pynput import keyboard
import threading
import ssl
import json

app = Flask(__name__)

POT = None
KEY = None
UNLOCKED = None

LOCK_SEQ = [3, 15, 2, 10, 8]
CURR_SEQ = []

JSON = "lockdata.json"

#route to collect most recent sequence
#in grafana: http://<your-ip>:3000/api/lock_sequences
@app.route('/api/lock_sequences', methods = ['GET'])
def curr_sequences():
    return JSON



def json_updater_thread():
    while True:
        sequences = {
            #Note: lock_seq is sent everytime everytime bc the json api plug in
            #in grafana does not keep record of previous queries
            "LOCK_SEQ": LOCK_SEQ,
            "CURR_SEQ": CURR_SEQ,
            "POT": POT,
            "UNLOCKED": UNLOCKED,
            "timestamp": int(time.time())
        }

        with open(JSON, "w") as f:
            json.dump(sequences, f, indent = 4)

        time.sleep(0.5)    


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to the ultrasonic ranger topic here
    client.subscribe("samardzi/pot")
    client.message_callback_add("samardzi/pot", pot_callback)

    print("Receiving Potentiometer data (MQTT)")

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def pot_callback(client, userdata, message):
    #if message.payloadFormatIndicator == 1:
    # print("rec: " + message.payload.decode('utf-8'))
    global POT 
    POT =  int(message.payload.decode('utf-8'))


# parallel task/thread to read keyboard input
def kbd_thread():
    global KEY
    while True:
        # must hit enter to complete the input
        k = input("")
        if k == 'a':
            client.publish("samardzi/key", "(click)")
            print("(click)")
            KEY = 1
        else:
            KEY = 0


if __name__ == '__main__':

    UNLOCKED = 0

    
    thread = threading.Thread(target=kbd_thread)
    json_thread = threading.Thread(target = json_updater_thread, daemon=True)
    # thread.daemon = True
    # start the thread executing
    thread.start()
    json_thread.start()

    

    client = mqtt.Client()

    # enable TLS, disable client-side certificates
    client.tls_set(
        tls_version = ssl.PROTOCOL_TLSv1_2
    )

    # begin connection
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="broker.emqx.io", port=8883, keepalive=60)
    # PORT 8883 enables TLS encryption for data using this socket.
    client.loop_start()

    #note: our in-lab stuff with grafana it said that grafana lstened on port 3000
    #by default, but idk if this will work may need to change
    app.run(host='0.0.0.0', port=3000)


    while True:
        #print("delete this line")
        time.sleep(0.5)


        #adds potentimeter value to list
        # if POT is 0 and button is pushed list is reset
        if(KEY == 1 and POT is not None):
            if(POT == 0):
                print("Resetting input.")
                CURR_SEQ.clear()
                UNLOCKED = 0
            else:
                print("++ " + str(POT))
                CURR_SEQ.append(POT)
                print("Current sequence:")
                print(CURR_SEQ)
            KEY = 0

        #if current sequence is equal to lock
        if(CURR_SEQ == LOCK_SEQ):
            print("Unlocked!")
            UNLOCKED = 1
            time.sleep(3)
            print("Resetting input")
            CURR_SEQ.clear()
            continue


        #if current sequence exceeds length
        if(len(CURR_SEQ) > len(LOCK_SEQ)):
            print("Failed; Resetting input.")
            UNLOCKED = 0
            CURR_SEQ.clear()
            time.sleep(1)
            print("Resetting Input")
            continue