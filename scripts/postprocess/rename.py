import os

# Root directory to start renaming
root_dir = "RLVC/KristenAndSara_1280x720_60"
print(f"Starting renaming in root directory: {root_dir}")
for dirpath, dirnames, filenames in os.walk(root_dir):
    print(f"Processing directory: {dirpath}")
    if "frames" not in dirpath:
        continue  # only process directories that have 'frames' in path
    for fname in filenames:
        if fname.lower().endswith(".png") and fname.startswith("im"):
            old_path = os.path.join(dirpath, fname)
            # Extract number part and remove leading zeros
            num_str = fname[2:-4]
            frame_number = int(num_str)
            # Convert to 'fXXX.png' with 3-digit padding
            new_fname = f"f{frame_number:03d}.png"
            new_path = os.path.join(dirpath, new_fname)
            os.rename(old_path, new_path)
            print(f"Renamed: {old_path} → {new_path}")