#! /usr/bin/python

# A simple Python command line tool to control an Omron MEMS Temp Sensor D6T-44L
# By Greg Griffes http://yottametric.com
# Modified by Iver Jordal
# GNU GPL V3 

# Jan 2015

import smbus
import sys
import getopt
import time 
import pigpio
from img_helper import write_image
from helpers import *
from time import sleep

i2c_bus = smbus.SMBus(1)
OMRON_1=0x0a                # 7 bit I2C address of Omron MEMS Temp Sensor D6T-44L
OMRON_BUFFER_LENGTH=35            # Omron data buffer size
data=[0]*OMRON_BUFFER_LENGTH    # initialize the temperature data list

# intialize the pigpio library and socket connection to the daemon (pigpiod)
pi = pigpio.pi()              # use defaults
version = pi.get_pigpio_version()
#print 'PiGPIO version = '+str(version)
handle = pi.i2c_open(1, 0x0a) # open Omron D6T device at address 0x0a on bus 1

#print "handle", handle

def tick(i2c_bus, OMRON_1, data):
   # initialize the device based on Omron's appnote 1
   result=i2c_bus.write_byte(OMRON_1,0x4c);

   (bytes_read, data) = pi.i2c_read_device(handle, len(data))

   #PTAT = convert_two_bytes_to_celsius(temperature_data[0], temperature_data[1])
   #print "PTAT:", PTAT

   celsius_data = []

   for i in range(2, 34, 2):
      temperature_celsius = convert_two_bytes_to_celsius(data[i], data[i+1])
      celsius_data.append(temperature_celsius)

   pretty_print_pixels(celsius_data)
   min_temp = min(celsius_data)
   max_temp = max(celsius_data)
   print 'min temp', min_temp
   print 'max temp', max_temp
   print 'difference between min and max', max_temp - min_temp
   lowest_values = get_six_lowest_values(celsius_data)
   median_of_lowest_values = median(lowest_values)
   print 'median of 6 lowest values', median_of_lowest_values
   print 'difference between median and max', max_temp - median_of_lowest_values
   img = convert_to_image(celsius_data)
   write_image('temperature.png', img)

try:
   for i in range(200):
      tick(i2c_bus, OMRON_1, data)
      sleep(0.25)
finally:
   print 'finally done'
   pi.i2c_close(handle)
   pi.stop()
