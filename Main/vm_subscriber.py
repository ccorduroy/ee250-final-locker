"""EE 250L Lab 04 Starter Code

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
from pynput import keyboard
import threading

POT = None
KEY = None
LOCK_SEQ = [3, 15, 2, 10, 8]
CURR_SEQ = []


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
    # setup the keyboard event listener
    # lis = keyboard.Listener(on_press=on_press)
    # lis.start() # start to listen on a separate thread

    thread = threading.Thread(target=kbd_thread)
    # thread.daemon = True
    # start the thread executing
    thread.start()

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="broker.emqx.io", port=1883, keepalive=60)
    client.loop_start()

    while True:
        #print("delete this line")
        time.sleep(0.5)

        #adds potentimeter value to list
        # if POT is 0 and button is pushed list is reset
        if(KEY == 1 and POT is not None):
            if(POT == 0):
                print("Resetting input.")
                CURR_SEQ.clear()
            else:
                print("++ " + str(POT))
                CURR_SEQ.append(POT)
                print("Current sequence:")
                print(CURR_SEQ)
            KEY = 0

        #if current sequence is equal to lock
        if(CURR_SEQ == LOCK_SEQ):
            print("Unlocked!")


        #if current sequence exceeds length
        if(len(CURR_SEQ) > len(LOCK_SEQ)):
            print("Failed; Resetting input.")
            CURR_SEQ.clear()