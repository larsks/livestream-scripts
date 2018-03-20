#!/bin/sh

# via https://projects.raspberrypi.org/en/projects/infrared-bird-box/12
raspivid \
	-awb sun \
	-ex auto \
	-co 20 \
	-br 60 \
	-o - -t 0 -w 1024 -h 768 -fps 25  -b 4000000 -g 50 -vf |
ffmpeg -loglevel warning -re -ar 44100 -ac 2 -acodec pcm_s16le -f s16le -ac 2 -i /dev/zero -f h264 -i - \
	-vcodec copy -acodec aac -ab 128k -g 50 -strict experimental -f flv rtmp://a.rtmp.youtube.com/live2/bbbp-ydpm-87tb-8pzx
