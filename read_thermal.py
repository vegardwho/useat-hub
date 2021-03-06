#! /usr/bin/python

# A simple Python command line tool to control an Omron MEMS Temp Sensor D6T-44L
# By Greg Griffes http://yottametric.com
# Modified by Iver Jordal
# GNU GPL V3 

# Jan 2015

import smbus
import sys
import getopt
import pigpio
from img_helper import write_image
from helpers import *
from time import sleep
import datetime
import hub_config

i2c_bus = smbus.SMBus(1)
OMRON_1 = 0x0a  # 7 bit I2C address of Omron MEMS Temp Sensor D6T-44L
OMRON_BUFFER_LENGTH = 35  # Omron data buffer size
data = [0] * OMRON_BUFFER_LENGTH  # initialize the temperature data list

# intialize the pigpio library and socket connection to the daemon (pigpiod)
pi = pigpio.pi()  # use defaults
version = pi.get_pigpio_version()
# print 'PiGPIO version = '+str(version)
handle = pi.i2c_open(1, 0x0a)  # open Omron D6T device at address 0x0a on bus 1

previous_celsius_data = []
last_movement_detected = datetime.datetime.now() - datetime.timedelta(minutes=10)
last_stationary_human_detected = datetime.datetime.now() - datetime.timedelta(minutes=10)
last_time_reported = datetime.datetime.now() - datetime.timedelta(minutes=10)


def tick(i2c_bus, OMRON_1, data):
    global previous_celsius_data, last_movement_detected, last_stationary_human_detected, last_time_reported

    i2c_bus.write_byte(OMRON_1, 0x4c)
    (bytes_read, data) = pi.i2c_read_device(handle, len(data))

    celsius_data = []

    for i in range(2, 34, 2):
        temperature_celsius = convert_two_bytes_to_celsius(data[i], data[i + 1])
        celsius_data.append(temperature_celsius)

    stationary = is_stationary_human(celsius_data)
    if stationary:
        last_stationary_human_detected = datetime.datetime.now()
    moving = is_moving_human(celsius_data, previous_celsius_data)
    if moving:
        last_movement_detected = datetime.datetime.now()
    recent_movement = last_movement_detected >= datetime.datetime.now() - get_frequency()
    recent_stationary = last_stationary_human_detected >= datetime.datetime.now() - get_frequency()
    human_detected_recently = recent_movement or recent_stationary
    is_available = not human_detected_recently
    #print 'last movement detected', last_movement_detected
    #print 'last stationary detected', last_stationary_human_detected
    #print 'is_available', is_available

    if last_time_reported <= datetime.datetime.now() - get_frequency():
        report_availability(hub_config.ROOM_ID, is_available, hub_config.HUB_TOKEN)
        last_time_reported = datetime.datetime.now()

    previous_celsius_data = celsius_data


try:
    while True:
        tick(i2c_bus, OMRON_1, data)
        sleep(0.25)
finally:
    #print 'finally done'
    pi.i2c_close(handle)
    pi.stop()
