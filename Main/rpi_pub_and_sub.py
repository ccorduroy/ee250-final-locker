"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time, sys
sys.path.append('../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd')
import grovepi

# --- ports
button = 1 #A1
potentiometer = 0 #A0
grovepi.pinMode(button, "INPUT")
grovepi.pinMode(potentiometer, "INPUT")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code " + str(rc))

    #subscribe to topics of interest here
    #client.subscribe("samardzi/button")    # add back callback
    #client.message_callback_add("samardzi/button", button_callback )

    print("Transmitting Potentiometer data (MQTT):")

#Default message callback. Please use custom callbacks.
#def on_message(client, userdata, msg):
    #print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#----------------------------------------------------------------------

if __name__ == '__main__':
    # this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="broker.emqx.io", port=1883, keepalive=60)
    client.loop_start()

    temp = 0

    while True:
        time.sleep(1)

        #read potentionmeter
        pot = grovepi.analogRead(potentiometer)
        num = int(pot / 103)     # splits potentiometer into 10 segments

        #only publish if there is a change in pot value
        if(num !=  temp):
            client.publish("samardzi/pot", num)
            temp = num
            print("curr: " + str(num))

        # if button pressed (HIGH signal detected), publish confirmation to button
        #if (grovepi.digitalRead(button) > 0):
            #client.publish("samardzi/button", 1)
            #print("confirm")

        #print(grovepi.digitalRead(button))

        #INSTALL: PIP INSTALL KEYBOARD
        #if(keyboard.is_pressed(KEY)):
            #client.publish("samardzi/button", 1)
            #print("confirm")