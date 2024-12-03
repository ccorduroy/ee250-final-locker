""" EE 250L Lab 02: GrovePi Sensors

Team members: Caitlin Sullivan, Isabella Samardzic

repo (https):
https://github.com/usc-ee250-fall2024/lab-02-grovepi-sensors-izzybeli.git

* Used Isabella's clone on Github Classroom for this assignment.
"""

"""python3 interpreters in Ubuntu (and other linux distros) will look in a 
default set of directories for modules when a program tries to `import` one. 
Examples of some default directories are (but not limited to):
  /usr/lib/python3.5
  /usr/local/lib/python3.5/dist-packages

The `sys` module, however, is a builtin that is written in and compiled in C for
performance. Because of this, you will not find this in the default directories.
"""

# goals of this assignment:
# - set a threshold distance by turning the rotary angle sensor
# - measure distance to an object using the ultrasonic sensor
# - determine whether the object is within threshold distance

import math, time, sys
# By appending the folder of all the GrovePi libraries to the system path here, we successfully `import grovepi`
sys.path.append('../../Software/Python/')
# This append is to support importing the LCD library.
sys.path.append('../../Software/Python/grove_rgb_lcd')
import grovepi
import grove_rgb_lcd

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

# --- potentiometer setup
#Rotary angle sensor connected to A0
potentiometer = 0
grovepi.pinMode(potentiometer, "INPUT")
time.sleep(1)

adc_ref = 5
grove_vcc = 5
max_dist = 517
max_pot = 1023

# --- ultrasonic ranger setup
# Connect the Grove Ultrasonic Ranger to digital port D4
ultrasonic_ranger = 4

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

# set display text \n for second line(or auto wrap)
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


"""This if-statement checks if you are running this python file directly. That 
is, if you run `python3 grovepi_sensors.py` in terminal, this if-statement will 
be true"""
if __name__ == '__main__':

    while True:
        try:
            #So we do not poll the sensors too quickly which may introduce noise,
            #sleep for a reasonable time of 200ms between each iteration.
            time.sleep(0.2)

            #read potentiometer and calculate current threshold
            # Read sensor value from potentiometer
            pot_raw = grovepi.analogRead(potentiometer)
            # Calculate distance (0 to 517) from potentiometer data (0 to 1023)
            threshold_dist = int(pot_raw * max_dist/max_pot)
            print("threshold: " + str(threshold_dist))

            # Read distance value from Ultrasonic
            curr_dist = grovepi.ultrasonicRead(ultrasonic_ranger)
            print("dist: " + str(curr_dist))

            # write to the LCD norefresh
            if curr_dist < threshold_dist:
                setText_norefresh(str(threshold_dist) + " OBJ PRES\n" + str(curr_dist) + "cm")
            else:
                setText_norefresh(str(threshold_dist) + "         \n" + str(curr_dist) + "cm")

            setRGB(0, 80, 160)     # background color turquoise
            # update previous as this iteration's current once done with the values to prep for next iter

        except IOError:
            print("IO Error")
        except TypeError:
            print("Type Error")
        except KeyboardInterrupt:
            break