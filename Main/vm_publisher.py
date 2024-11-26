"""EE 250L Lab 04 Starter Code

Run vm_publisher.py in a separate terminal on your VM."""

import paho.mqtt.client as mqtt
import time
from pynput import keyboard
import threading

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))
    #subscribe to topics of interest here

#Default message callback. Please use custom callbacks.
def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

# parallel task/thread to read keyboard input
def kbd_thread():
        while True:
            # must hit enter to complete the input
            k = input("")
            if k == 'w':
                print("w")
                # send "w" character to rpi
                client.publish("samardzi/lcd", "w")
            elif k == 'a':
                print("a")
                # send "a" character to rpi
                # subscribe
                client.publish("samardzi/led", "LED_ON")
                client.publish("samardzi/lcd", "a")
                # send "LED_ON"
            elif k == 's':
                print("s")
                # send "s" character to rpi
                client.publish("samardzi/lcd", "s")
            elif k == 'd':
                print("d")
                # send "d" character to rpi
                # send "LED_OFF"
                client.publish("samardzi/led", "LED_OFF")
                client.publish("samardzi/lcd", "d")


if __name__ == '__main__':
    #setup the keyboard event listener
    #lis = keyboard.Listener(on_press=on_press)
    #lis.start() # start to listen on a separate thread

    thread = threading.Thread(target=kbd_thread)
    #thread.daemon = True
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
        time.sleep(1)
            

