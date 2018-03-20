#!/bin/sh

: ${FFMPEG_LOGLEVEL:=warning}
: ${FFMPEG_VIDEO_SIZE:=1024x768}

v4l2-ctl \
	-c brightness=60 \
	-c contrast=10 \
	-c vertical_flip=1 \
	-c white_balance_auto_preset=6

ffmpeg -hide_banner -loglevel $FFMPEG_LOGLEVEL -re \
	-ar 44100 -ac 2 -acodec pcm_s16le \
	-f s16le -ac 2 -i /dev/zero \
	-f v4l2 -input_format h264 -video_size $FFMPEG_VIDEO_SIZE -i /dev/video0 \
	-vcodec copy -acodec aac -ab 128k -g 50 -strict experimental \
	-f flv rtmp://a.rtmp.youtube.com/live2/bbbp-ydpm-87tb-8pzx
