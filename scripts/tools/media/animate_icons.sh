#!/bin/bash
# Maya's Icon Animator - Bypasses Cinnamon's static icon limit by cycling files
# Usage: ./animate_icons.sh /path/to/animated.webp /path/to/static_target.png

ANIM_SRC="$1"
TARGET_ICON="$2"

if [ ! -f "$ANIM_SRC" ]; then echo "Source not found"; exit 1; fi

# Extract frames to a temp directory
mkdir -p /tmp/maya_anim
ffmpeg -y -i "$ANIM_SRC" -vf "scale=256:256" /tmp/maya_anim/frame_%03d.png > /dev/null 2>&1

while true; do
    for frame in /tmp/maya_anim/frame_*.png; do
        cp "$frame" "$TARGET_ICON"
        # Trigger a refresh hint for the file manager
        touch "$TARGET_ICON"
        sleep 0.1
    done
done
