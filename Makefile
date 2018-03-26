PIP = pip3
INSTALL = install
SYSTEMCTL = systemctl

all:

install: install-scripts install-python install-units

install-scripts:
	$(INSTALL) -m 755 livestream.sh /usr/local/bin/livestream

install-python:
	$(PIP) install $(PIPFLAGS) .

install-units: install-services

install-services:
	$(INSTALL) -m 644 systemd/livestream.service \
		/etc/systemd/system/livestream.service

daemon-reload:
	$(SYSTEMCTL) daemon-reload
