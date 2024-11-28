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


#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

#Default message callback. Please use custom callbacks.
def callback_button(client, userdata, msg):
    print("[" + msg.topic + "]" + str(msg.payload, "utf-8"))

#Default message callback. Please use custom callbacks.
def callback_pot(client, userdata, msg):
    print("[" + msg.topic + "]" + str(msg.payload, "utf-8"))

#----------------------------------------------------------------------

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.loop_start()

    temp = 0

    while True:
        time.sleep(1)

        #read potentionmeter
        pot = grovepi.analogRead(potentiometer)
        number = pot / 1

        #only publish if there is a change in pot value
        if(number !=  temp):
            #client.publish("samardzi/potentiometer", number)
            temp = number
            print(number)

        # if button pressed (HIGH signal detected), publish confirmation to button
        if (grovepi.digitalRead(button) > 0):
            #client.publish("samardzi/button", 1)
            print("confirm")