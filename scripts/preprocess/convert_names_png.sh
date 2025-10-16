#!/bin/bash
base_dir="/WAVE/users2/unix/wkong/compress396/project2/datasets_cropped/ClassD-416x240"

find "$base_dir" -type f -name "f*.png" | while read file; do
    dir=$(dirname "$file")
    base=$(basename "$file" .png)

    # Extract number after "im"
    num=${base#f}

    # Remove leading zeros, then pad to 3 digits
    num=$((10#$num))
    newnum=$(printf "%03d" "$num")

    mv "$file" "$dir/f${newnum}.png"
done
