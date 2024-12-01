"""EE 250L Lab 04 Starter Code

Run vm_subscriber.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time

POT = None
BUTTON = None
LOCK_SEQ = [3, 15, 2, 10, 8]
CURR_SEQ = []


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to the ultrasonic ranger topic here
    client.subscribe("samardzi/potentiometer")
    client.message_callback_add("samardzi/potentiometer", pot_Callback)

    #subribe to button
    client.subscribe("samardzi/button")
    client.message_callback_add("samardzi/button", button_Callback)

    print("subscribed to USR, button")

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def pot_Callback(client, userdata, message):
    #if message.payloadFormatIndicator == 1:
    print("Locked in: " + message.payload.decode('utf-8'))
    global POT 
    POT =  int(message.payload.decode('utf-8'))



def button_Callback(client, userdata, message):
    #if message.payloadFormatIndicator == 1:
    print(message.payload.decode('utf-8'))
    global BUTTON
    BUTTON = int(message.payload.decode('utf-8'))

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="broker.emqx.io", port=1883, keepalive=60)
    client.loop_start()

    while True:
        #print("delete this line")
        time.sleep(1)

        #adds potentimeter value to list.
        #if POT is 0 and button is pushed
        #list is reset
        if(BUTTON == 1):
            if(POT == 0):
                print("List Reset")
                CURR_SEQ.clear()
            else:
                CURR_SEQ.append(POT)
                print(CURR_SEQ)

        #if current sequence is equal to lock
        if(CURR_SEQ == LOCK_SEQ):
            print("Unlocked!!")


        #if current sequenxy exceeds length
        if(len(CURR_SEQ) > len(LOCK_SEQ)):
            print("failure")
            CURR_SEQ.clear()
        

            



