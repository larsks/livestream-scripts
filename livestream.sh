#!/bin/sh

: ${FFMPEG_LOGLEVEL:=warning}
: ${FFMPEG_THREAD_QUEUE_SIZE:=256}

if [ -z "$YOUTUBE_STREAM_KEY" ]; then
	echo "ERROR: missing youtube stream key" >&2
	exit 1
fi

pycam \
	${CAMERA_AWB:+--awb $CAMERA_AWB} \
	${CAMERA_BRIGHTNESS:+--brightness $CAMERA_BRIGHTNESS} \
	${CAMERA_CONTRAST:+--contrast $CAMERA_CONTRAST} \
	${CAMERA_FRAMERATE:+--fps $CAMERA_FRAMERATE} \
	${CAMERA_VFLIP:+--vflip} \
	${CAMERA_HFLIP:+--hflip} \
	${CAMERA_RESOLUTION:+--resolution $CAMERA_RESOLUTION} |
ffmpeg -hide_banner -loglevel $FFMPEG_LOGLEVEL -re \
	-ar 44100 -ac 2 -acodec pcm_s16le \
	-f s16le -ac 2 -i /dev/zero \
	-thread_queue_size $FFMPEG_THREAD_QUEUE_SIZE \
	-f h264 -i - \
	-vcodec copy -acodec aac -ab 128k -g 50 -strict experimental \
	-f flv rtmp://a.rtmp.youtube.com/live2/${YOUTUBE_STREAM_KEY}
