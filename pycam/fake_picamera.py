import logging
import time

LOG = logging.getLogger(__name__)


class PiCamera:
    AWB_MODES = {'dummy': 0}

    def __init__(self, **kwargs):
        LOG.warning('You are using the fake picamera module. If you are '
                    'running this code on a raspberry pi, please install '
                    'the picamera module.')

    def start_recording(self, output, **kwargs):
        pass

    def stop_recording(self, **kwargs):
        pass

    def wait_recording(self, t):
        time.sleep(t)
