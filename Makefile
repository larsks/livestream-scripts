INSTALL = install
SYSTEMCTL = systemctl

all:

install: install-scripts install-units

install-scripts:
	$(INSTALL) -m 755 uv4l-updateoverlay.sh /usr/local/bin/uv4l-updateoverlay

install-units: install-services install-timers install-config

install-config:
	$(INSTALL) -m 644 uv4l/uv4l-raspicam.conf /etc/uv4l/uv4l-raspicam.conf
	$(INSTALL) -m 644 uv4l/text_template.json /etc/uv4l/text_template.json

install-services:
	$(INSTALL) -m 644 systemd/uv4l-updateoverlay.service \
		/etc/systemd/system/uv4l-updateoverlay.service

install-timers:
	$(INSTALL) -m 644 systemd/uv4l-updateoverlay.timer \
		/etc/systemd/system/uv4l-updateoverlay.timer

daemon-reload:
	$(SYSTEMCTL) daemon-reload

activate-timers:
	$(SYSTEMCTL) enable --now uv4l-updateoverlay.timer
