#!/usr/bin/env python
# -*- coding: utf-8 -*-
# alarm_clock.py
'''Machine
alarm_clock is very simple machine for test and training.

AditNW LLC, Redmond , WA
www.AditNW.com
'''

# rev Z0.18
# rev Z0.26 - modifying on laptop with new cam
# rev z0.30 - modify to use updated voyager


# standard library
from dataclasses import dataclass
from time import sleep
import datetime as dt
from datetime import datetime
import pytz

# modules in local folder
import my_RPi_config as config
from critter_cam_detect import Object_Detector

#### Imports to support custom code in root directory
import importlib

# import key utilities
rpi_utilities = importlib.import_module('.machines.rpi_utilities', package='RPi_voyager')
rpi_API = rpi_utilities.utilities
machine_utilities = importlib.import_module('.machines.machine_utilities', package='RPi_voyager')
machine_API = machine_utilities.utilities
scroll_defaults = machine_utilities.scroll_defaults
rpi_recorder = importlib.import_module('.recorder', package='RPi_voyager')
RPi_Camera = rpi_recorder.RPi_Camera
return_time_stamp = rpi_recorder.return_time_stamp


#Testing to replace this:  from ..recorder import RPi_Camera, return_time_stamp


#### Define the GPIO for the board
# Each GPIO function must be defined here
# The pin numbers can be over-ridden by the config file (this allows a common
# machine module to support different machines with different pinouts but to
# use the same logic)
# IMPORTANT:  PIN #'s are BCM, not board.  There is no provision for using 
# board numbering in RPi_Voyager

## Format for pins varies slightly by function
# LED: [function, pin#, 'LED', False]
# Button: [None, pin#, 'button', False] name and pin# matter only
# Servo: [None, pin#, 'servo', 0] - last value is initial position (-1 to 1)
gpio_func = {
    'pulse LED': [None, 13, 'LED', False],
    'red LED': [None, 5, 'LED', False],
    'blue LED 1': [None, 10, 'LED', False],
    'blue LED 2': [None, 11, 'LED', False],
    'button1' : [None, 27, 'button', False],
}


@dataclass
class Goop():
    '''do not call just data
    '''
    usb_path: int = 99

    total_photos: int=0

    # sensor acquired data
    data_record_details = {}

    def __post_init__(self):
        '''runs as an init
        '''
        pass

    def update_sensor_data(self, sensor_mgr):
        pass

    def check_goop(self):
        '''testing method for seeing all values in __dict__
        '''
        print('Goop __dict__')
        for key, value in self.__dict__.items():
            print(key, ': ', value)


class Brain():
    def __init__(self, goop):
        # assign names to objects that were instantiated in mechanic
        self.goop = goop

        ### instantiate key drivers and managers
        # these are filled by mechanic
        self.driver = None
        self.lcd_mgr = None
        self.sensor_mgr = None
        self.data_rcdr = None

        #### init Camera
        # recorder_camera is a voyager object, not the camera
        # the actual camera object is recorder_camera.camera
        self.recorder_camera = RPi_Camera()

        # use the actual camera object so Object Detector can actuate it
        self.detector = Object_Detector(self.recorder_camera.camera)
        self.take_photos = config.START_TAKING_PHOTOS
        self.photo_burst_count = 0
        self.photo_inhibit = 0  # photos are inhibited if greater than 0 (this sets
                                # to the DELAY_AFTER_BURST for delay in minutes)

    def start_up_actions(self):
        '''method is called by mechanic
        Place actions here to be started after drivers are instantiated but
        before timers are started
        '''
        pass



        ###################################
        ####   Display Called Functions####
        ###################################
    def start_display(self):
        '''initiate display and do first display
        '''
        pass

        ####################
        ####   Timing   ####
        ####################

    def timers(self, sched_maker):
        '''Timers for alarm_clock
        '''
        #### tik functions are called on even seconds, tok on odd
        self.tik = True
        sched_maker.create_timer('every second', self.tiktok)

        #### every poll (.1 in schedule-machine):
        

        #### every Second
        # must call display scroll in case clock or data are present
        #sched_maker.create_timer('every second', self.display_scroll)


        #### every Minute
        #sched_maker.create_timer('every minute', self.check_backlight)

        #### system timers
        sched_maker.create_timer('on the 5 second', self.driver.execute_gpio)
        sched_maker.create_timer('on the 5 second', self.update_goop_data)
        # sched_maker.create_timer('on the 15 second', self.data_rcdr.record_data)


        #### Camera Timers
        sched_maker.create_timer('on the 5 second', self.critter_capture)
        sched_maker.create_timer('on the 15 second', self.photo_counter)
        sched_maker.create_timer('every minute', self.minute_functions)
        sched_maker.create_timer('on the 5 minute', self.zero_photo_burst)

        sched_maker.create_timer('on the 15 second', self.focus_capture)


        ##############################
        #### TIMER action methods ####
        ##############################

    def photo_counter(self):
        ''' Photo Counter 2x Blue LED
        LED 1 ON: 1 - 9 photo
        LED 2 ON: 10 - 99 photos
        LED 1 & 2 ON: 100+ photos
        '''
        #print(f'total photos: {self.detector.total_photos}: burst_count: {self.photo_burst_count}, photo_inhibit: {self.photo_inhibit}\n')
        if self.detector.total_photos < 1:
            self.driver.direct_drive_gpio('blue LED 1', 'off', None)
            self.driver.direct_drive_gpio('blue LED 2', 'off', None)
        elif 1 <= self.detector.total_photos < 10:
            self.driver.direct_drive_gpio('blue LED 1', 'on', None)
            self.driver.direct_drive_gpio('blue LED 2', 'off', None)
        elif 10 <= self.detector.total_photos < 100:
            self.driver.direct_drive_gpio('blue LED 1', 'off', None)
            self.driver.direct_drive_gpio('blue LED 2', 'on', None)
        else:
            self.driver.direct_drive_gpio('blue LED 1', 'on', None)
            self.driver.direct_drive_gpio('blue LED 2', 'on', None)
        

    def zero_photo_burst(self):
        '''makes sure burst delay isn't triggered over long period
        '''
        self.photo_burst_count = 0

    def minute_functions(self):
        #### increment_burst_delay
        if self.photo_inhibit >= 0:
            self.photo_inhibit -=1
            self.driver.direct_drive_gpio('red LED', 'blink', (.25, .25))
        
        if self.photo_inhibit <= 0:
            self.photo_inhibit = 0
            self.driver.direct_drive_gpio('red LED', 'off', None)

        #### One Minute Report
        print('\n\n#### minute report ####')
        # cpu tempurature
        cpu_temp = rpi_API.get_cpu_temp()
        print(f'cpu temp: {cpu_temp:.0f}')
        images_size = rpi_API.get_directory_size("./my_images", use_cwd=True)
        print(f'my_images size: {images_size} MB')
        print(f'total photos: {self.detector.total_photos}: burst_count: {self.photo_burst_count}, photo_inhibit: {self.photo_inhibit}\n')



    def critter_capture(self):
        '''Basic photo analysis and capture method
        step 1: get an analysis image
        step 2: frame_detect is the TensorFlow analysis
        step 3: if take_photo is True, performs a capture
        '''
        if self.take_photos == True and self.photo_inhibit < 1:
            self.driver.direct_drive_gpio('red LED', 'on', None)

            # get image and convert to use for TensorFlow
            # image is prepped image
            image = self.detector.get_analysis_image()

            # Analyze the image against the detect list and indicate if photo
            # should be taken.
            # take_photo is boolean as to if a photo was captured or not
            take_photo, object_name, score = self.detector.frame_detect(image)

            if config.DEBUG == True: print(f'take_photo: {take_photo}, object_name: {object_name}')

            self.driver.direct_drive_gpio('red LED', 'off', None)
            if take_photo == True:
                self.driver.direct_drive_gpio('blue LED 1', 'blink', (.5, .5))
                self.driver.direct_drive_gpio('blue LED 2', 'blink', (.5, .5))

                #### take photo
                self.detector.take_HD_photo(object_name, score)

                self.photo_burst_count += 1
                if self.photo_burst_count >= config.PHOTOS_PER_BURST:
                    self.photo_inhibit = config.DELAY_AFTER_BURST + 1
                    self.driver.direct_drive_gpio('red LED', 'blink', (.25, .25))

                self.take_photo = False
        else:
            # focus captures are in separate method to allow different timing
            pass

    def focus_capture(self):
        '''very simple capture for accessing image.jpg to check setup
        '''
        if self.take_photos == False:
            if config.DEBUG == True: print('take focus photo image.jpg')
            self.detector.take_focus_photo()


    def update_goop_data(self):
        self.goop.update_sensor_data(self.sensor_mgr)

    def tiktok(self):
        if self.tik == True:
            self.driver.direct_drive_gpio('pulse LED', 'on', None)
            #print('+')
            self.tik = False
        else:
            self.driver.direct_drive_gpio('pulse LED', 'off', None)
            #print('-', end='')
            self.tik = True



        ##########################
        #### Button Functions ####
        ##########################
    def execute_button_function(self, action):
        '''executes actions from button held
        Only allows a single next action
        Next action is run by timer
        '''
        if self.next_action == None:
            self.next_action = action
        




        ###############################
        #### Button Action Methods ####
        ###############################

    def button1_pressed_function(self):
        # light LED just to indicate button is pressed
        self.driver.direct_drive_gpio('red LED', 'on', None)


    def button1_released_function(self):
        self.driver.direct_drive_gpio('red LED', 'off', None)
        self.take_photos = not self.take_photos
        if self.take_photos == True:
            print('\n\n#### START Taking Photos ####')
        else:
            print('\n\n#### STOP Taking Photos ####')


    def button1_hold_function(self):
        #### shutdown RPi when held
        print('\n### initiating shutdown')
        # delay before shutdown should allow all functions to stop
        self.take_photos = False
        for i in range(0, 5):
            self.driver.direct_drive_gpio('blue LED 1', 'on', None)
            self.driver.direct_drive_gpio('blue LED 2', 'on', None)
            self.driver.direct_drive_gpio('red LED', 'on', None)
            self.driver.direct_drive_gpio('pulse LED', 'on', None)

            sleep(.5)
            self.driver.direct_drive_gpio('blue LED 1', 'off', None)
            self.driver.direct_drive_gpio('blue LED 2', 'off', None)
            self.driver.direct_drive_gpio('red LED', 'off', None)
            self.driver.direct_drive_gpio('pulse LED', 'off', None)
            sleep(.5)

        print('\n\n !!!! Shut Down !!!!')
        self.recorder_camera.close_camera()
        sleep(1)
        rpi_API.shutdownRPI()


    #### Button 2 ####
    def button2_pressed_function(self):
        pass

    def button2_released_function(self):
        pass

    def button2_hold_function(self):
        pass


    #### Button 3 ####
    def button3_pressed_function(self):
        pass

    def button3_released_function(self):
        pass

    def button3_hold_function(self):
        pass


    







    