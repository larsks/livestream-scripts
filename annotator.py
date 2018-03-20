#!/usr/bin/python3

import picamera
import datetime
import sys

datefmt = '%Y-%m-%d %H:%M'

camera = picamera.PiCamera(
    resolution=(854, 480),
    framerate=24)
camera.vflip = 1
camera.brightness = 60
camera.contrast = 10
camera.awb_mode = 'sunlight'
camera.annotate_background = picamera.Color('black')
camera.annotate_text = datetime.datetime.now().strftime(datefmt)

camera.start_recording(sys.stdout.buffer,
    format='h264',
    )

try:
    while True:
        camera.annotate_text = datetime.datetime.now().strftime(datefmt)
        camera.wait_recording(60)
except KeyboardInterrupt:
    pass

camera.stop_recording()
