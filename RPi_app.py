#!/usr/bin/env python
# -*- coding: utf-8 -*-
# RPi_app.py
'''RPi_app.py initiates the app factory in RPi_voyager
Using your my_RPi_config file, RPi_app builds a custom
app to run your Raspberry Pi headless with GPIO.

AditNW LLC, Redmond , WA
www.AditNW.com
'''

__author__ = 'Brad Allen, AditNW LLC'

import signal
from RPi_voyager import create_machine

machine = create_machine()

def keyboardInterruptHandler(signal, frame):
    '''safe handle ctl-c stop'''
    exit(0)

def remote_startUp():
    '''function for call from startUpProgram
    This allows auto start up from a common file
    Can also be called in differentdirectory in RPi'''
    signal.signal(signal.SIGINT, keyboardInterruptHandler)
    machine.run()

if __name__ == "__main__":
	# react to keyboard interrupt
    signal.signal(signal.SIGINT, keyboardInterruptHandler)

    machine.run()


