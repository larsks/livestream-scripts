#!/bin/bash

# Parse overlay config
file=$(sed -rne '/^text-filename.*=/{s/^text-filename *= *(.*)$/\1/g;p}' /etc/uv4l/uv4l-raspicam.conf)

[[ "$file" == "" ]] && { echo "no configured overlay file"; exit 1; }

# Parse template
sed -re "s|\\\$time|`date '+%D %H:%M'`|g" </etc/uv4l/text_template.json >${file}

# Update overlay text
v4l2-ctl --set-ctrl=text_overlay=1 &>/dev/null
