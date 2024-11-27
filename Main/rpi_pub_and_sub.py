"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time, sys
sys.path.append('../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd')
import grovepi

# --- ports
button = 3 #A3
potentiometer = 0 #A0
grovepi.pinMode(button, "INPUT")
grovepi.pinMode(potentiometer, "INPUT")



#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))


#----------------------------------------------------------------------

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.loop_start()

    while True:
        time.sleep(1)

        #read potentionmeter
        pot = grovepi.analogRead(potentiometer)

        #only publish if change was made
        if(pot !=  temp):
            client.publish("samardzi/potentiometer", pot)
            temp = pot


        # if button pressed(HIGH signal detected)
        if (grovepi.digitalRead(button) > 0):
            client.publish("samardzi/button", "Button Pressed!")
            