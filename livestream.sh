#!/bin/sh

: ${CAMERA_BRIGHTNESS:=50}
: ${CAMERA_CONTRAST:=0}
: ${CAMERA_AWB:=6}
: ${CAMERA_VFLIP:=0}
: ${CAMERA_HFLIP:=0}

: ${FFMPEG_LOGLEVEL:=warning}
: ${FFMPEG_VIDEO_SIZE:=1024x768}
: ${FFMPEG_FRAMERATE:=20}

v4l2-ctl \
	-c brightness=$CAMERA_BRIGHTNESS \
	-c contrast=$CAMERA_CONTRAST \
	-c vertical_flip=$CAMERA_VFLIP \
	-c horizontal_flip=$CAMERA_HFLIP \
	-c white_balance_auto_preset=$CAMERA_AWB

ffmpeg -hide_banner -loglevel $FFMPEG_LOGLEVEL -re \
	-ar 44100 -ac 2 -acodec pcm_s16le \
	-f s16le -ac 2 -i /dev/zero \
	-f v4l2 -input_format h264 -video_size $FFMPEG_VIDEO_SIZE -framerate $FFMPEG_FRAMERATE -i /dev/video0 \
	-vcodec copy -acodec aac -ab 128k -g 50 -strict experimental \
	-f flv rtmp://a.rtmp.youtube.com/live2/bbbp-ydpm-87tb-8pzx
