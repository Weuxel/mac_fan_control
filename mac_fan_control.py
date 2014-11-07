#!/usr/bin/python2 -W ignore::Warning
# coding=utf8

__author__="Norman Riess <norman@smash-net.org>"
__date__ ="$30.10.2014$"

# Required:
# applesmc kernel module
# Python 2 as python-daemon does not work for Python 3
# dev-python/python-daemon

import sys
import os
import signal
import daemon
import daemon.pidfile
import time

FAN_PATH = "/sys/devices/platform/applesmc.768/fan1"
TEMP_SENSOR_CORE_1 = "/sys/devices/platform/applesmc.768/temp5"
TEMP_SENSOR_CORE_2 = "/sys/devices/platform/applesmc.768/temp15"
TEMP_HOT = 80

PID_FILE="/var/run/mac_fan_control.pid"


def get_value(file_name):
	
    value_file = open(file_name, "r")
    value = int(value_file.readline())
    value_file.close()
	
    return value


def set_value(file_name, value):

    try:
        value_file = open(file_name, "w")
        value_file.write(str(value))
        value_file.flush()
    except IOError, e:
        pass
    finally:    
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

        # Activate manual fan control if needed
        if get_value(FAN_PATH + "_manual") != 1: set_value(FAN_PATH + "_manual", "1")
		
        # Temperature of the cores
        temp_core_1 = get_value(TEMP_SENSOR_CORE_1 + "_input")
        temp_core_2 = get_value(TEMP_SENSOR_CORE_2 + "_input")
        
        # <temp> as the hottest core
        if temp_core_1 > temp_core_2: temp = temp_core_1
        else: temp = temp_core_2
        
        # Compare temperatures und set the fan speed
        if temp in range(temp_hot, temp_hot + 3000): pass
        elif temp > temp_hot:
            rotation += 100
            if rotation > fan_max: rotation = fan_max
        else:
            rotation -= 100
            if rotation < fan_min: rotation = fan_min
        set_value(FAN_PATH + "_output", rotation)

        # Wait x seconds
        time.sleep(5)


def daemonize():
	
    with daemon.DaemonContext(pidfile=daemon.pidfile.PIDLockFile(PID_FILE)):
        main()


def stop():

    try:
        pid = get_value(PID_FILE)
        os.kill(pid, signal.SIGQUIT)
        os.remove(PID_FILE)
    except OSError, e:
        print(str(e))
    except IOError, e:
        print(str(e))


def usage():

    print
    print("Usage:")
    print("./mac_fan_control.py <start|stop>")
    print


if __name__ == "__main__":

    if len(sys.argv) == 2:
        if "start" == sys.argv[1]:
            daemonize()
        elif "stop" == sys.argv[1]:
            stop()
        else:
            usage()
            sys.exit(1)
    else:
        usage()
        sys.exit(1)