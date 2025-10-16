#!/bin/bash

# Set the root directory for the dataset
dataset_dir="/WAVE/users2/unix/wkong/compress396/project2/datasets"

# Find all files matching f*.png and loop through them
find "$dataset_dir" -type f -name "f*.png" | while read file; do
    # Get the directory path and the base filename (without the .png extension)
    dir=$(dirname "$file")
    base=$(basename "$file" .png)

    # Extract the number part by removing the 'f' prefix (e.g., "f001" -> "001")
    num=${base#f}

    # Convert the number to a base-10 integer to handle leading zeros correctly
    num_int=$((10#$num))

    # Create the new base filename with an "im" prefix and 5-digit zero padding
    printf -v new_base "im%05d" "$num_int"

    # Perform the move/rename operation and print the change
    mv "$file" "$dir/${new_base}.png"
    echo "Renamed: $file -> $dir/${new_base}.png"
done

echo "Renaming complete."