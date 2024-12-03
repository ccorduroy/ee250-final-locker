""" EE 250 Final Project: VM Pubsub
- handles primary computations and data processing
- manages JSON export of important information
- data is collected from rpi_pubsub.py via encrypted MQTT

THIS SCRIPT IS WHERE MOST OF YOUR INTERACTION HAPPENS. KEEP THIS WINDOW OPEN TO SEE BACKEND STATISTICS
AND HANDLE KEYPRESS EVENTS.
"""

import paho.mqtt.client as mqtt
import time, os
from pynput import keyboard
import threading
import ssl
import json

# globals
POT = None
KEY = None
UNLOCKED = None
RESET = None

LOCK_SEQ = [1, 2, 3, 4]
CURR_SEQ = []

# change name to your file ->
JSON = "lockdata.json"

# -----------------------------------------------------------------

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to the ultrasonic ranger topic here
    client.subscribe("samardzi/pot")
    client.message_callback_add("samardzi/pot", pot_callback)

    client.subscribe("samardzi/keys")
    client.message_callback_add("samardzi/keys", key_callback)

    print("Receiving Potentiometer data (MQTT)")

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def pot_callback(client, userdata, message):
    #if message.payloadFormatIndicator == 1:
    # print("rec: " + message.payload.decode('utf-8'))
    global POT 
    POT =  int(message.payload.decode('utf-8'))

def key_callback(client, userdata, message):
    rec =  message.payload.decode('utf-8')
    print("key: " + rec)
    global KEY
    if rec == "frontend_rec":
        KEY = 1
    else:
        KEY = 0

# -----------------------------------------------------------------

# parallel task/thread to read keyboard input
def kbd_thread():
    global KEY
    global RESET
    while True:
        # must hit enter to complete the input
        k = input("")
        if k == 'a':
            client.publish("samardzi/keys", "(click)")
            print("(click)")
            KEY = 1
        elif k == 'd':
            RESET = 1
        else:
            KEY = 0

# -----------------------------------------------------------------

def json_updater_thread():
    # update JSON file on a timer with new values
    while True:
        data = {
            "current number": POT,
            "current sequence": CURR_SEQ,
            "solution sequence": LOCK_SEQ,
            "is unlocked": UNLOCKED,
            "timestamp": int(time.time())
        }

        with open(JSON, "w") as f:
            json.dump(data, f, indent = 4)

        time.sleep(0.5) # update every 0.5s

# -----------------------------------------------------------------

if __name__ == '__main__':

    UNLOCKED = 0

    thread = threading.Thread(target=kbd_thread)
    json_thread = threading.Thread(target=json_updater_thread, daemon=True)
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

    while True:
        #print("delete this line")
        time.sleep(0.5)

        #adds potentimeter value to list
        # if POT is 0 and button is pushed list is reset
        if(KEY == 1 and POT is not None):
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
            print("Resetting Input.")
            CURR_SEQ.clear()

# TODO: separate reset button on keyboard - do this on testbed branch
        if (RESET == 1):
            print("Resetting input.")
            CURR_SEQ.clear()
            UNLOCKED = 0
            RESET = 0

        #failure state
        if(len(CURR_SEQ) >= len(LOCK_SEQ)) and (CURR_SEQ != LOCK_SEQ):
            print("Failed")
            CURR_SEQ.clear()
            UNLOCKED = 0
            print("Resetting Input.")