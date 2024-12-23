"""EE 250L Lab 04 Starter Code

Run rpi_pubsub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time, sys
sys.path.append('../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd')
import grovepi
import ssl

# --- ports
button = 1 #A1
potentiometer = 0 #A0
grovepi.pinMode(button, "INPUT")
grovepi.pinMode(potentiometer, "INPUT")

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code " + str(rc))

    #subscribe to topics of interest here
    client.subscribe("samardzi/keys")    # add back callback
    client.message_callback_add("samardzi/keys", key_callback )

    print("Transmitting Potentiometer data (MQTT):")

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def key_callback(client, userdata, message):
    #if message.payloadFormatIndicator == 1:
    print(message.payload.decode('utf-8'))

#----------------------------------------------------------------------

if __name__ == '__main__':

    client = mqtt.Client()

    # enable TLS, disable client-side certificates
    client.tls_set(
        tls_version = ssl.PROTOCOL_TLSv1_2
    )

    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="broker.emqx.io", port=8883, keepalive=60)
    # PORT 8883 enables TLS encryption for data using this socket.
    client.loop_start()

    temp = 0

    while True:
        time.sleep(0.25)

        #read potentiometer
        pot = grovepi.analogRead(potentiometer)
        num = int(pot / 103)     # splits potentiometer into 10 segments

        #only publish if there is a change in pot value
        if(num !=  temp):
            client.publish("samardzi/pot", num)
            temp = num
            print("curr: " + str(num))