#!/usr/bin/python3

import click
import logging
import datetime
import sys

try:
    import picamera
except ImportError:
    from pycam import fake_picamera as picamera

AWB_MODES = picamera.PiCamera.AWB_MODES
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


def validate_rotation(ctx, param, value):
    if value is None:
        return

    value = int(value)
    if value in [0, 90, 180, 270]:
        return value

    raise click.BadParameter('rotation must be one of 0, 90, 180, 270')


@click.command()
@click.option('-R', '--resolution', type=click.Choice(RESOLUTIONS.keys()))
@click.option('-h', '--height', type=int)
@click.option('-w', '--width', type=int)
@click.option('-b', '--bitrate', type=int)
@click.option('-r', '--rotate', type=int, callback=validate_rotation)
@click.option('--vflip', is_flag=True)
@click.option('--hflip', is_flag=True)
@click.option('-f', '--framerate', type=float)
@click.option('--format', default='h264')
@click.option('-B', '--brightness', type=int, default=50)
@click.option('-C', '--contrast', type=int, default=0)
@click.option('-W', '--awb-mode', type=click.Choice(AWB_MODES))
@click.option('--an', '--annotate-text')
@click.option('--as', '--annotate-text-size', type=int)
@click.option('--ab', '--annotate-background')
@click.option('--ai', '--annotate-interval', type=float, default=60)
@click.option('--debug', 'loglevel', flag_value='DEBUG')
@click.option('--verbose', 'loglevel', flag_value='INFO', default=True)
@click.option('--quiet', 'loglevel', flag_value='WARNING')
@click.option('-o', '--output', type=click.File(mode='wb'),
              default=sys.stdout.buffer)
def cli(resolution, height, width, bitrate, rotate, vflip, hflip,
        format, framerate, brightness, contrast, awb_mode,
        annotate_text, annotate_text_size, annotate_background,
        annotate_interval, loglevel, output):
    logging.basicConfig(level=loglevel)

    camera_kwargs = {}

    if resolution:
        camera_kwargs['resolution'] = RESOLUTIONS[resolution]
    elif width is not None and height is not None:
        camera_kwargs['resolution'] = (width, height)

    if framerate is not None:
        camera_kwargs['framerate'] = framerate

    LOG.info('initializing camera with %s', camera_kwargs)
    camera = picamera.PiCamera(**camera_kwargs)

    camera_config = {
        'vflip': vflip,
        'hflip': hflip,
        'brightness': brightness,
        'contrast': contrast,
        'awb_mode': awb_mode,
        'rotation': rotate,
    }

    LOG.info('configuring camera with %s', camera_config)
    for k, v in camera_config.items():
        if v is not None:
            setattr(camera, k, v)

    if annotate_text:
        camera.annotate_text = datetime.datetime.now().strftime(annotate_text)
        if annotate_background is not None:
            camera.annotate_background = picamera.Color(annotate_background)
        if annotate_text_size is not None:
            camera.annotate_text_size = annotate_text_size

    record_kwargs = {}

    if bitrate is not None:
        record_kwargs['bitrate'] = bitrate
    if format is not None:
        record_kwargs['format'] = format

    LOG.info('start recording with %s', record_kwargs)
    camera.start_recording(output, **record_kwargs)

    try:
        while True:
            if annotate_text:
                text = datetime.datetime.now().strftime(annotate_text)
                LOG.debug('update annotation: %s', text)
                camera.annotate_text = text
            camera.wait_recording(annotate_interval)
    finally:
        camera.stop_recording()


def main():
    cli(auto_envvar_prefix='CAMERA')
