#!/bin/bash

for f in *.jpg *.jpeg *.png; do
  [ -f "$f" ] || continue
  out="${f%.*}.webp"

  echo "Processing $f → $out"

  ffmpeg -i "$f" -filter_complex "[0:v]scale=512:512:force_original_aspect_ratio=increase,crop=512:512,setsar=1,format=yuva420p,geq=lum='p(X,Y)':a='if(gt(sqrt(pow(X-W/2,2)+pow(Y-H/2,2)),W/2),0,255)'[v]" \
  -map "[v]" -vcodec libwebp -loop 0 -lossless 0 -compression_level 6 -q:v 80 "$out"
done