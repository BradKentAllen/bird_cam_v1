# config.py for detect_PiCam




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




