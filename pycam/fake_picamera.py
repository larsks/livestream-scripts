import logging
import time

LOG = logging.getLogger(__name__)

errmsg = '''You are using the fake picamera module. If you are
running this code on a Raspberry Pi, please install
the picamera module (https://picamera.readthedocs.io/).

On Raspbian, you may install the module by running:

    apt-get install python3-picamera

'''


class PiCamera:
    AWB_MODES = {'dummy': 0}

    def __init__(self, **kwargs):
        LOG.warning(errmsg)

    def start_recording(self, output, **kwargs):
        pass

    def stop_recording(self, **kwargs):
        pass

    def wait_recording(self, t):
        time.sleep(t)
