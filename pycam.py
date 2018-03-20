#!/usr/bin/python3

import argparse
import logging
import picamera
import datetime
import sys

LOG = logging.getLogger(__name__)

RESOLUTIONS = {
    '2160p': (3840, 2160),
    '1440p': (2560, 1440),
    '1080p': (1920, 1080),
    '720p': (1280, 720),
    '480p': (854, 480),
    '360p': (640, 360),
    '240p': (426, 240),
}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--hflip',
                   action='store_true')
    p.add_argument('--vflip',
                   action='store_true')
    p.add_argument('--width', '-W',
                   type=int,
                   default=854)
    p.add_argument('--height', '-H',
                   type=int,
                   default=480)
    p.add_argument('--resolution', '-r',
                   choices=RESOLUTIONS.keys())
    p.add_argument('--framerate', '--fps',
                   type=int,
                   default=30)
    p.add_argument('--brightness', '--br',
                   type=int)
    p.add_argument('--contrast', '--co',
                   type=int)
    p.add_argument('--awb-mode', '--awb',
                   choices=picamera.PiCamera.AWB_MODES.keys())

    g = p.add_argument_group('Output')
    g.add_argument('--output', '-o',
                   type=argparse.FileType('wb'),
                   default=sys.stdout.buffer)

    g = p.add_argument_group('Annotation')
    g.add_argument('--annotate', '-a',
                   default='%Y-%m-%d %H:%M')
    g.add_argument('--annotate-background', '-g',
                   default='black')
    g.add_argument('--annotate-interval', '-i',
                   type=int,
                   default=60)
    g.add_argument('--no-annotate',
                   dest='annotate',
                   action='store_const',
                   const=None)

    g = p.add_argument_group('Logging')
    g.add_argument('--verbose', '-v',
                   dest='loglevel',
                   action='store_const',
                   const='INFO')
    g.add_argument('--quiet', '-q',
                   dest='loglevel',
                   action='store_const',
                   const='WARNING')
    g.add_argument('--debug',
                   dest='loglevel',
                   action='store_const',
                   const='DEBUG')

    p.set_defaults(loglevel='INFO')

    return p.parse_args()


def main():
    args = parse_args()
    logging.basicConfig(level=args.loglevel)

    if args.resolution:
        args.width, args.height = RESOLUTIONS[args.resolution]

    LOG.info('initializing camera with resolution=(%dx%d), framerate=%d',
             args.width, args.height, args.framerate)
    camera = picamera.PiCamera(
        resolution=(args.width, args.height),
        framerate=args.framerate)

    if args.vflip is not None:
        LOG.info('vflip = %d', args.vflip)
        camera.vflip = args.vflip
    if args.hflip is not None:
        LOG.info('hflip = %d', args.hflip)
        camera.hflip = args.hflip
    if args.brightness is not None:
        LOG.info('brightness = %d', args.brightness)
        camera.brightness = args.brightness
    if args.contrast is not None:
        LOG.info('constrast = %d', args.contrast)
        camera.contrast = args.contrast
    if args.awb_mode is not None:
        LOG.info('awb_mode = %s', args.awb_mode)
        camera.awb_mode = args.awb_mode

    if args.annotate is not None:
        camera.annotate_text = datetime.datetime.now().strftime(args.annotate)
        if args.annotate_background is not None:
            camera.annotate_background = picamera.Color(
                args.annotate_background)

    camera.start_recording(args.output, format='h264')

    try:
        while True:
            LOG.debug('update annotation')
            camera.annotate_text = datetime.datetime.now().strftime(args.annotate)
            camera.wait_recording(args.annotate_interval)
    except KeyboardInterrupt:
        pass

    camera.stop_recording()


if __name__ == '__main__':
    main()
