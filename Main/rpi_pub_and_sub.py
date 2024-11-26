"""EE 250L Lab 04 Starter Code

Run rpi_pub_and_sub.py on your Raspberry Pi."""

import paho.mqtt.client as mqtt
import time, sys
sys.path.append('../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd')
import grovepi
import grove_rgb_lcd

# --- ports
led = 4
ultrasonic_ranger = 5
button = 3
grovepi.pinMode(button, "INPUT")
grovepi.pinMode(led, "OUTPUT")
# --- RGB LCD setup
if sys.platform == 'uwp':
    import winrt_smbus as smbus
    bus = smbus.SMBus(1)
else:
    import smbus
    import RPi.GPIO as GPIO
    rev = GPIO.RPI_REVISION
    if rev == 2 or rev == 3:
        bus = smbus.SMBus(1)
    else:
        bus = smbus.SMBus(0)

# LCD has two I2C addresses:
DISPLAY_RGB_ADDR = 0x62
DISPLAY_TEXT_ADDR = 0x3e

# --- RGB LCD Utilities
# ----------------------------------------------------------------------
# set backlight to (R,G,B) (values from 0..255 for each)
def setRGB(r,g,b):
    bus.write_byte_data(DISPLAY_RGB_ADDR,0,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,1,0)
    bus.write_byte_data(DISPLAY_RGB_ADDR,0x08,0xaa)
    bus.write_byte_data(DISPLAY_RGB_ADDR,4,r)
    bus.write_byte_data(DISPLAY_RGB_ADDR,3,g)
    bus.write_byte_data(DISPLAY_RGB_ADDR,2,b)

# send command to display (no need for external use)
def textCommand(cmd):
    bus.write_byte_data(DISPLAY_TEXT_ADDR,0x80,cmd)

def setText(text):
    textCommand(0x01) # clear display
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))

#Update the display without erasing the display
def setText_norefresh(text):
    textCommand(0x02) # return home
    time.sleep(.05)
    textCommand(0x08 | 0x04) # display on, no cursor
    textCommand(0x28) # 2 lines
    time.sleep(.05)
    count = 0
    row = 0
    while len(text) < 32: #clears the rest of the screen
        text += ' '
    for c in text:
        if c == '\n' or count == 16:
            count = 0
            row += 1
            if row == 2:
                break
            textCommand(0xc0)
            if c == '\n':
                continue
        count += 1
        bus.write_byte_data(DISPLAY_TEXT_ADDR,0x40,ord(c))\
#----------------------------------------------------------------------

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #subscribe to topics of interest here
    client.subscribe("samardzi/led")    # add back callback
    client.message_callback_add("samardzi/led", led_callback )

    client.subscribe("samardzi/lcd")
    client.message_callback_add("samardzi/lcd", lcd_callback)

    print("subscribed to LED, LCD")

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

def lcd_callback(client, userdata, message):
    #print letter given
    #if message.payloadFormatIndicator == 1:
    letter = (message.payload).decode('utf-8')
    setText(letter)

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

        setRGB(0, 80, 160)

        dat = grovepi.ultrasonicRead(ultrasonic_ranger)
        client.publish("samardzi/ultrasonicRanger", dat)
        #print("USR: " + dat)
        #client.publish("samardzi/button", "connection OK")


        # if button pressed(HIGH signal detected)
        if (grovepi.digitalRead(button) > 0):
            client.publish("samardzi/button", "Button Pressed!")