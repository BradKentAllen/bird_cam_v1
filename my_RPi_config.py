#!/usr/bin/env python
# -*- coding: utf-8 -*-
# my_RPi_config.py
'''Follow the commented instructions, below, to create your custom
Raspberry Pi app.

AditNW LLC, Redmond , WA
www.AditNW.com
'''

#### letter refers to RPi_voyager revision
# a revised letter rev requires review of configs
# voyager rev: Z-0.0.1
# voyager rev: Z0.0.15 - schedule_machine timers
# rev Z0.26 - modifying on laptop with new cam



	####################################
	#### (0.0) Operational Settings ####
	####################################
# Settings that modify how the machine operates within normal parameters.
# These settings are used to tune how the machine operates (as opposed to setting
# up the machine like the rest are used for).  These settings are not checked by
# the configuration check.
# determines if camera starts on or off (False is off)
START_TAKING_PHOTOS = True

DELAY_AFTER_BURST = 1	# time in minutes between looking for next shots

PHOTOS_PER_BURST = 5		# photos taken when motion detected

DELAY_BETWEEN_PHOTOS = 2	# seconds between photos in a burst

#CAMERA_RESOLUTION = (2592, 1944)  # pi camera V2
CAMERA_RESOLUTION = (4056, 3040)   # pi camera HQ
CAMERA_EXPOSURE_MODE = 'sports'

PHOTO_SET = 5     # will take five photos before pause
PHOTO_PAUSE = 60  # seconds will pause after photo_set

USE_DETECT_LIST = True
detect_list = [
            'bird',
            'cat',
            'dog',
            'teddy bear'
            'horse',
            'sheep',
            'cow',
            'elephant',
            'bear',
            'zebra',
            'giraffe',
            #'person',
            ]

#### TensorFlow model information
TENSOR_FLOW_RESOLUTION = (300, 300)
MIN_CONF_THRESHOLD = .5
MODEL_NAME = 'coco_ssd_mobilenet_v1'
GRAPH_NAME = 'detect.tflite'
LABELMAP_NAME = 'labelmap.txt'

	################################
	#### (1.0) General Settings ####
	################################

#### (1.1) # Names
NAME = 'CC' 			# string in quotes
MACHINE = 'custom_machine'	# DO NOT CHANGE the machine unless you are doing
							# development.  Refer to the documents for this value.

#### (1.1.1) # Custom Code Reference
CUSTOM_MACHINE_CODE = 'critter_cam'

#### (1.2) # Time Zone
local_time_zone = 'US/Pacific'

# XXXX for UTC: 
# 'US/Aleutian', 'US/Hawaii', 'US/Alaska', 'US/Arizona', 'US/Michigan'
# 'US/Pacific', 'US/Mountain', 'US/Central', 'US/Eastern'




#### (1.2) # Development Tools
# Validate - runs a data validation of all config parameters and constants 
# prior to operation.  Typically just used during development
# Works with DEBUG.  If DEBUG is True, exceptions will be raised one at a time in the console.
# If DEBUG is False then my_RPi_config is fully checked and problems in my_RPi_config 
# will be displayed on the RPi display.  Machine function may or may not continue depending
# on if that config problem causes an error.
VALIDATE_CONFIG = True 	# True/False

# If DEBUG = True
# For use when testing RPi using command line
# Will give results in print statements for locating issues
# During config file validation, results are printed not sent to LCD and each error will stop
# operation and raise a ConfigValueError.
DEBUG = True



#### (1.3) # Communication Interfaces (USB and WIFI)
# In order to use USB drives, must have set up RPi with usbmount
# This includes installing usbmount and modifying /lib/systemd/system/systemd-udevd.service
USB_MOUNT = False

# wifi_auto moves the RPi wpa_supplicant from USB to the drive then to use for wifi
# usb_mount must be True for this to work, as a USB drive is required
WIFI_AUTO = False


 

	##############################
	#### (2.0) Hardware Setup ####
	##############################

#### (2.1) # RPi pins
# RPi_voyager uses the BCM pin numbering nomenclature
# BCM corresponds to the processor, not the RPi board
# These are non-sequentially numbered pins on most diagrams

RPi_PINOUT_BCM = {
    'pulse LED': 13,
    'red LED': 5,
    'blue LED 1': 10,
    'blue LED 2': 11,
    'button1' : 27,
	}

#### (2.2) # RPi GPIO
# pigpio is an alternative control for the RPi gpio
# pigpio provides more stable hardware pulse width modulations
# when using servos
# The pigpio daemon must be running for this to work
# To enable and will run on boot:
# sudo systemctl enable pigpiod
USE_PIGPIO = False


	##################################
	#### 3.0 UI, Buttons, Display ####
	##################################

#### (3.1) # LCD setup
# 'I2C/16x2', 'I2C/20x4', 'wired/16x2', None
LCD_TYPE = None

#### (3.1.1) # LCD Custom Characters
# Custom characters can only be used that are defined within RPi_voyager
# see documents for defined custom characters

#### (3.2) # Buttons
# button pullup is True if button connects input to ground
# button pullup is False if button connects input to 3V3
button_pull_up = False

# button hold time is used for time it takes to hold a button for a function
button_hold_time = 5


#### (3.3) # Scroll interface

 


	#####################################################
	#### (4.0) Sensors, Data, Data Recorder, Logging ####
	#####################################################
#### (4.1) # Sensor List 
# select from Available Sensors in list below for this machine
# full senosr details are in the documentation
# some sensors use Adafruit drivers which must be individually loaded
SENSOR_LIST = [ ]

# (4.1.1) Available sensors on this machine:
# 'HIH6121' - Honeywell tempurature and RH
#HIH6121_I2C_address = 0x27	# this is probably 0x27

#### (4.2) # Units

# saves data and recovers when restarts
# can be False or an integer number of minutes
# number of minutes is how often the data is saved
SAVE_BETWEEN_SESSIONS = False

# data logger
data_file_name = 'data_log'
DATA_FILE_TITLE = 'Alarm Clock Data'
RECORD_DATA = 'all'		# all or list of data parameter names and their titles {'RH': 'RH', 'tempF': 'F', 'tempC': 'C'} 
RECORD_CSV = False
RECORD_TXT = False
RECORD_TO_SD = True
RECORD_TO_USB = False

# file manage mode can be: 'one file/keep all', 'one file/record over', 'new file each run'
FILE_MANAGE_MODE = 'one file/keep all'
FILE_LINE_LIMIT = 10	# only keeps last ten lines
DAILY_HEADER = False

# data logger formatting (primarily for .txt file)
TIME_SPACE = 12		# Space allotted for time column

# details for each type of data to be recorded
# Name is official name for that data and must be available from an active sensor
# Tuple format:  ('column title, number of spaces for column as integer)
DATA_RECORD_DETAILS = {
    } 



	###############################
	#### (5.0) Output Hardware ####
	###############################
####


	########################################
	#### 6.0 Unique Function Parameters ####
	########################################
####


	##############################
	#### (7.0) Custom Methods ####
	##############################
# define as many custom functions as you would like
# define in standard python
# these must be defined before the my_timed_functions dictionary


'''
import importlib
recorder = importlib.import_module('.recorder', package='RPi_voyager')

camera_box = recorder.Camera()

def camera_func():
	print('\n\n$$$$ TAKE PHOTO  $$$$')
	camera_box.take_photo()
'''


	######################
	#### (8.0) Timers ####
	######################
####

#### my_timed_functions dictionary is used to index and define timers
# two ways to enter timing:
# At time intervals: ('seconds', 10, function), ('minutes', 15, function), ('hour', None, function)
# Note:  for longer than 1 hour interval, use minutes such as 120 for two hours
# At a specific time: ('at a time', '23:30', function)
# We have found you will avoid time zone issues with daylight savings time
# if you avoid having actions exactly at 00:00 (midnight)
#
# IMPORTANT:  the function is passed in this dictionary so carefully follow the use
# of quotes
my_timed_functions = {
	#'my_func1' : ('on the 15 second', my_func1),
	#'my_func2' : ('schedule', my_func2, '11:55'),
	#'camera_func' : ('on the 15 second', camera_func),
	}







