#!/bin/bash

dataset_dir="/WAVE/users2/unix/wkong/compress396/project2/datasets/ClassD-416x240/BlowingBubbles_416x240_50"

find "$dataset_dir" -type f -name "*.png" | while read -r file; do
    dir=$(dirname "$file")
    base=$(basename "$file" .png)

    # Ensure the base name is numeric (skip if not)
    if [[ "$base" =~ ^[0-9]+$ ]]; then
        num=$base
        printf -v new_base "f%03d" "$num"
        mv "$file" "$dir/${new_base}.png"
    fi
done
