# detect_PICamD.py
# explore specializing for birds

'''Critter_Cam detect is TensorFlow logic for critter_cam
'''

# rev 0.1   initial dev
# rev 0.2   separate photo and detect logic


# Import packages
import os
import io
import argparse
#import cv2
import numpy as np
import sys
import time
#from threading import Thread
import importlib.util

from picamera import PiCamera
from PIL import Image
from time import sleep, time

import my_RPi_config as config

class Object_Detector:
    def __init__(self, camera):
        self.total_photos = 0   # total photos taken this session
        self.min_conf_threshold = config.MIN_CONF_THRESHOLD

        self.camera = camera

        # this the data from the camera
        self.stream = io.BytesIO()

        #### create detect_dict from detect_list
        # detect_dict counts how many of each is captured
        self.detect_dict = {}
        for item in config.detect_list:
            self.detect_dict[item] = 1


        # Import TensorFlow libraries
        # If tflite_runtime is installed, import interpreter from tflite_runtime, else import from regular tensorflow
        pkg = importlib.util.find_spec('tflite_runtime')
        if pkg:
            from tflite_runtime.interpreter import Interpreter
        else:
            from tensorflow.lite.python.interpreter import Interpreter

        # Get path to current working directory
        CWD_PATH = os.getcwd()

        # Path to .tflite file, which contains the model that is used for object detection
        PATH_TO_CKPT = os.path.join(CWD_PATH, config.MODEL_NAME, config.GRAPH_NAME)

        # Path to label map file
        PATH_TO_LABELS = os.path.join(CWD_PATH, config.MODEL_NAME, config.LABELMAP_NAME)

        # Load the label map
        with open(PATH_TO_LABELS, 'r') as f:
            self.labels = [line.strip() for line in f.readlines()]

        # Have to do a weird fix for label map if using the COCO "starter model" from
        # https://www.tensorflow.org/lite/models/object_detection/overview
        # First label is '???', which has to be removed.
        if self.labels[0] == '???':
            del(self.labels[0])

        # Load the Tensorflow Lite model.
        self.interpreter = Interpreter(model_path=PATH_TO_CKPT)

        self.interpreter.allocate_tensors()

        # Get model details
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        self.height = self.input_details[0]['shape'][1]
        self.width = self.input_details[0]['shape'][2]

        self.floating_model = (self.input_details[0]['dtype'] == np.float32)

        self.input_mean = 127.5
        self.input_std = 127.5


    def frame_detect(self, frame_resized):
        ''' determine if item in detect list is in frame
        '''
        if config.DEBUG == True: start_time = time()

        #### parameters used if photo is taken
        take_photo = False          # True is to take photo of object
        object_name = 'no photo'    # First object detected in list
        score = 0                   # score for that object

        # convert frame to numpy array
        input_data = np.expand_dims(frame_resized, axis=0)

        # Normalize pixel values if using a floating model (i.e. if model is non-quantized)
        if self.floating_model:
            input_data = (np.float32(input_data) - self.input_mean) / self.input_std

        # Perform the actual detection by running the model with the image as input
        self.interpreter.set_tensor(self.input_details[0]['index'],input_data)
        self.interpreter.invoke()

        # Retrieve detection results
        boxes = self.interpreter.get_tensor(self.output_details[0]['index'])[0] # Bounding box coordinates of detected objects
        classes = self.interpreter.get_tensor(self.output_details[1]['index'])[0] # Class index of detected objects
        scores = self.interpreter.get_tensor(self.output_details[2]['index'])[0] # Confidence of detected objects
        #num = interpreter.get_tensor(output_details[3]['index'])[0]  # Total number of detected objects (inaccurate and not needed)

        ##### List objects for debug
        '''
        print(f'\n total objects: {len(scores)}')
        for i in range(len(scores)):
            print(f'[{self.labels[int(classes[i])]}, {scores[i]:.2f}]')
        print('\n')
        '''
        
        # Loop over all detections and draw detection box if confidence is above minimum threshold
        for i in range(len(scores)):
            if ((scores[i] > self.min_conf_threshold) and (scores[i] <= 1.0)):
                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1,(boxes[i][0] * int(config.CAMERA_RESOLUTION[1]))))
                xmin = int(max(1,(boxes[i][1] * int(config.CAMERA_RESOLUTION[0]))))
                ymax = int(min(int(config.CAMERA_RESOLUTION[1]),(boxes[i][2] * int(config.CAMERA_RESOLUTION[1]))))
                xmax = int(min(int(config.CAMERA_RESOLUTION[0]),(boxes[i][3] * int(config.CAMERA_RESOLUTION[0]))))
                
                # Draw label
                this_object_name = self.labels[int(classes[i])] # Look up object name from "labels" array using class index

                xcenter = xmin + (int(round((xmax - xmin) / 2)))
                ycenter = ymin + (int(round((ymax - ymin) / 2)))

                #print('Object ' + str(i) + ': ' + object_name + ' at (' + str(xcenter) + ', ' + str(ycenter) + ')')
                if config.DEBUG == True: print(f'Object {str(i)}: {object_name}, score: {scores[i]:.2f}')

                #### Take photo if in the detect dict
                if this_object_name in self.detect_dict:
                    # only place take_photo can become True
                    take_photo = True

                    # tag using the object with the highest score
                    if scores[i] > score:
                        score = scores[i]
                        object_name = this_object_name
                    
                # XXXX this should not be required with the highest score portion above
                # break if photo should be taken (this also solidifies the object_name)
                '''
                if take_photo == True:
                    break
                '''

        # XXXX DEBUG function timer
        if config.DEBUG == True:
            elapsed_time = time() - start_time
            print(f'detect time: {elapsed_time:.2f}')

        return take_photo, object_name, score


    def take_HD_photo(self, object_name, score):
        show_score = int(100 * score)
        if config.DEBUG == True: print(f'\n\n >>>> take photo of {object_name}, score: {show_score} <<<<')

        file_name = './my_images/' + object_name + '_' + str(self.detect_dict[object_name]) + '_' + str(show_score) + '.jpg'
        self.camera.capture(file_name)
        self.detect_dict[object_name] +=1
        self.total_photos += 1

    def take_focus_photo(self):
        self.camera.capture('/home/pi/image.jpg')
     

    def get_analysis_image(self):
        '''step 1 in detect
        Takes photo and compresses it to proper size for TensorFlow
        '''
        # uses PiCamera to capture from stream
        # total time: 2.2 seconds
        if config.DEBUG == True: start_time = time()
        self.camera.capture(self.stream, 'jpeg')
        self.stream.seek(0)
        
        # captures from stream and formats for Tensor Flow
        # time: 1016 ms
        image = Image.open(self.stream).convert('RGB').resize((config.TENSOR_FLOW_RESOLUTION[0] , config.TENSOR_FLOW_RESOLUTION[1]),
                             Image.ANTIALIAS)

        self.stream.seek(0)
        self.stream.truncate()

        if config.DEBUG == True:
            elapsed_time = time() - start_time
            print(f'image process time: {elapsed_time:.2f} ', end='')

        return image


                    
if __name__ == '__main__':
    print('\n\n################')
    print('detect_PiCamC.py rev 0.7')

    RPi_camera = PiCamera()
    RPi_camera.resolution = config.CAMERA_RESOLUTION
    RPi_camera.exposure_mode = config.CAMERA_EXPOSURE_MODE

    sleep(2)    # let gain control settle
    
    print(f'resolution: {RPi_camera.resolution}')
    print(f'iso: {RPi_camera.iso}')
    print(f'exposure: {RPi_camera.exposure_mode}')

    

    detector = Object_Detector(RPi_camera)
    
    

    last_time = 0
    while True:
        print('need to fix this')

        # manage to one frame check per second
        wait_time = 1 - (time() - last_time)
        if wait_time > 0:
            sleep(wait_time)

        last_time = time()

        #sleep(.7)
        #input('return for photo')
        







