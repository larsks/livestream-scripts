PIP = pip3
INSTALL = install
SYSTEMCTL = systemctl

all:

install: install-scripts install-units

install-scripts: install-pycam
	$(INSTALL) -m 755 livestream.sh /usr/local/bin/livestream

install-pycam:
	$(PIP) install $(PIPFLAGS) .

install-units: install-services install-config

install-config:

install-services:
	$(INSTALL) -m 644 systemd/livestream.service \
		/etc/systemd/system/livestream.service

daemon-reload:
	$(SYSTEMCTL) daemon-reload
