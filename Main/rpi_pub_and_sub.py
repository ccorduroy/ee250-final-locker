"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time, sys
sys.path.append('../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd')
import grovepi

# --- ports
button = 3
grovepi.pinMode(button, "INPUT")
grovepi.pinMode(led, "OUTPUT")


def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("samardzi/led")    # add back callback
    client.message_callback_add("samardzi/led", led_callback )

    print("subscribed to LED")

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def led_callback(client, userdata, message):
    #if message .payloadFormatIndicator == 1:
    if message.payload.decode('utf-8') == "LED_ON":
        digitalWrite(led, 1)
        print("LED ON")
    elif message.payload.decode('utf-8') == "LED_OFF":
        digitalWrite(led, 0)

#----------------------------------------------------------------------

if __name__ == '__main__':
    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="broker.emqx.io", port=1883, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)

        dat = grovepi.ultrasonicRead(ultrasonic_ranger)
        client.publish("samardzi/ultrasonicRanger", dat)
        print("USR LOCAL: " + dat)

        # if button pressed(HIGH signal detected)
        if (grovepi.digitalRead(button) > 0):
            client.publish("samardzi/button", "Button Pressed!")