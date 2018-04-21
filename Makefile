PIP = pip3
INSTALL = install
SYSTEMCTL = systemctl

SOCKETS = \
	systemd/camera-ffmpeg.socket \
	systemd/camera-raw.socket

SERVICES = \
	systemd/camera-ffmpeg@.service \
	systemd/camera-raw@.service \
	systemd/camera-tee.service \
	systemd/livestream.service

all:

install: install-scripts install-python install-units

install-scripts:
	$(INSTALL) -m 755 livestream.sh /usr/local/bin/livestream

install-python:
	$(PIP) install $(PIPFLAGS) .

install-units: install-sockets install-services

install-sockets: $(SOCKETS)
	for unit in $^; do \
		$(INSTALL) -m 644 $$unit /etc/systemd/system/; \
	done

install-services: $(SERVICES)
	for unit in $^; do \
		$(INSTALL) -m 644 $$unit /etc/systemd/system/; \
	done

daemon-reload:
	$(SYSTEMCTL) daemon-reload
