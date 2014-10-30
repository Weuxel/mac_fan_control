#!/usr/bin/python2 -W ignore::Warning
# coding=utf8

__author__="Norman Riess <norman@smash-net.org>"
__date__ ="$30.10.2014$"

# Required:
# Python 2 as python-daemon does not work for Python 3
# dev-python/python-daemon

import daemon
import time

def main():
	while True:
		print("Juhu")
		time.sleep(2)

def daemonize():
	
	with daemon.DaemonContext():
		main()

if __name__ == "__main__":
    daemonize()