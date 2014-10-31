#!/usr/bin/python2 -W ignore::Warning
# coding=utf8

__author__="Norman Riess <norman@smash-net.org>"
__date__ ="$30.10.2014$"

# Required:
# applesmc kernel module
# Python 2 as python-daemon does not work for Python 3
# dev-python/python-daemon

import daemon
import time

FAN_PATH = "/sys/devices/platform/applesmc.768/fan1"
TEMP_SENSOR_CORE_1 = "/sys/devices/platform/applesmc.768/temp5"
TEMP_SENSOR_CORE_2 = "/sys/devices/platform/applesmc.768/temp15"
TEMP_HOT = 80


def get_value(file_name):
	
    value_file = open(file_name, "r")
    value = int(value_file.readline())
    value_file.close()
	
    return value


def set_value(file_name, value):

    value_file = open(file_name, "w")
    value_file.write(str(value))
    value_file.flush()
    value_file.close()


def main():

    # Fan min and max rotations per second
    fan_min = get_value(FAN_PATH + "_min")		
    fan_max = get_value(FAN_PATH + "_max")

    # Initially set min rotation
    rotation = fan_min
    set_value(FAN_PATH + "_output", rotation)

    # Preparing temperature to compare
    temp_hot = TEMP_HOT * 1000

    while True:

        print("Schleifenbeginn")
	
        # Activate manual fan control if needed
        if get_value(FAN_PATH + "_manual") != 1: set_value(FAN_PATH + "_manual", "1")
		
        # Temperature of the cores
        temp_core_1 = get_value(TEMP_SENSOR_CORE_1 + "_input")
        temp_core_2 = get_value(TEMP_SENSOR_CORE_2 + "_input")
        
        # <temp> as the hottest core
        if temp_core_1 > temp_core_2: temp = temp_core_1
        else: temp = temp_core_2

        print("Temp: " + str(temp))
        
        # Compare temperatures und set the fan speed
        if temp in range(temp_hot, temp_hot + 3000): print("Pass")
        elif temp > temp_hot:
            rotation += 100
            if rotation > fan_max: rotation = fan_max
        else:
            rotation -= 100
            if rotation < fan_min: rotation = fan_min
        set_value(FAN_PATH + "_output", rotation)

        print("Rotation: " + str(rotation))

        # Wait x seconds
        time.sleep(5)


def daemonize():
	
    with daemon.DaemonContext():
        main()

if __name__ == "__main__":
    #daemonize()
    main()