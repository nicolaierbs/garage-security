import cv2
import logging
import time
from datetime import datetime, timedelta
from pathlib import Path
import configparser
import sys

params = configparser.ConfigParser()
params.read('parameters.ini')
image_path = params.get('STORAGE', 'path')
sleep_time = params.getint('VIDEOS', 'sleep_time')
capture_time = params.getint('VIDEOS', 'capture_time')
brightness = params.getfloat('VIDEOS', 'brightness')


def configure_logger():
    logger = logging.getLogger('standard_logger')
    logger.setLevel(logging.DEBUG)
    # create file handler which logs even debug messages
    fh = logging.FileHandler('debug.log')
    fh.setLevel(logging.DEBUG)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)
    return logger


def hierarchical_file(date, suffix):
    path = image_path + date.strftime("%Y/%m/%d/%H/")
    Path(path).mkdir(parents=True, exist_ok=True)
    return path + str(int(date.timestamp())) + '.' + suffix


def lights(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    return hsv[:, :, 2].mean() > brightness


def take_images():
    # initialize the camera
    cam = cv2.VideoCapture(1)   # 0 -> index of camera
    # Obtain frame size information using get() method
    frame_width = int(cam.get(3))
    frame_height = int(cam.get(4))
    frame_size = (frame_width, frame_height)
    fps = 20

    log.info('Initialized camera capturing')
    captured = True
    while captured:
        captured, img = cam.read()
        time.sleep(sleep_time)
        if lights(img):
            log.info('Detected light')
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(hierarchical_file(datetime.now(), 'mp4'),
                                  fourcc, fps, frame_size)
            end_time = datetime.now() + timedelta(seconds=capture_time)
            while datetime.now() < end_time:
                ret, frame = cam.read()
                out.write(frame)
            out.release()

        elif not captured:
            log.error('No image captured')
            sys.exit(1)


log = configure_logger()
log.info('Started camera_capturer')
take_images()
log.info('End camera-capturer')
