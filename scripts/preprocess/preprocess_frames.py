import os
from PIL import Image

dataset_path = "/WAVE/users2/unix/wkong/compress396/project2/datasets/ClassD-416x240/BlowingBubbles_416x240_50"
output_path = "/WAVE/users2/unix/wkong/compress396/project2/datasets/ClassD-416x240/BlowingBubbles_416x240_50"

def make_multiple_of_64(x):
    return (x // 64) * 64  # floor to nearest multiple of 64

for root, _, files in os.walk(dataset_path):
    for f in files:
        if f.endswith(".png"):
            img_path = os.path.join(root, f)
            img = Image.open(img_path)

            # Ensure 3 channels
            if img.mode != "RGB":
                img = img.convert("RGB")

            w, h = img.size
            new_w, new_h = make_multiple_of_64(w), make_multiple_of_64(h)

            # Crop top-left corner to nearest multiple of 64
            img_cropped = img.crop((0, 0, new_w, new_h))

            # Prepare output directory
            out_dir = root.replace(dataset_path, output_path)
            os.makedirs(out_dir, exist_ok=True)

            # Save the processed image
            img_cropped.save(os.path.join(out_dir, f))
