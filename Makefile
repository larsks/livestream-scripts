INSTALL = install
SYSTEMCTL = systemctl

all:

install: install-scripts install-units

install-scripts:
	$(INSTALL) -m 755 livestream.sh /home/pi/livestream.sh

install-units: install-services install-timers install-config

install-config:

install-services:
	$(INSTALL) -m 644 systemd/livestream.service \
		/etc/systemd/system/livestream.service

daemon-reload:
	$(SYSTEMCTL) daemon-reload
