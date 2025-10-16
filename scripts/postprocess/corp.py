import cv2
import os

# -------------------------
# Root folders
# -------------------------
rlvc_root = "/Users/wenhankong/Downloads/temp/RLVC"
dcvc_root = "/Users/wenhankong/Downloads/temp/DCVC/reconstructed_frames_psnr"
output_root = "/Users/wenhankong/Downloads/temp/cropped_output"
os.makedirs(output_root, exist_ok=True)

# -------------------------
# Sequences configuration
# Each sequence has:
#   - RLVC lambda folder (user selects PSNR lambda)
#   - DCVC quality (user selects quality index)
# -------------------------
sequences = {
    "ClassB_BasketballDrive": {
        "folder": "BasketballDrive_1920x1072_50",
        "rlvc_lambda_folder": "BasketballDrive_1920x1072_50_PSNR_256",
        "dcvc_quality": 1
    },
    "ClassC_PartyScene": {
        "folder": "PartyScene_832x480_50",
        "rlvc_lambda_folder": "PartyScene_832x480_50_PSNR_512",
        "dcvc_quality": 1
    },
    "ClassD_BQSquare": {
        "folder": "BQSquare_416x240_60",
        "rlvc_lambda_folder": "BQSquare_416x240_60_PSNR_512",
        "dcvc_quality": 1
    },
    "ClassE_KristenAndSara": {
        "folder": "KristenAndSara_1280x720_60",
        "rlvc_lambda_folder": "KristenAndSara_1280x720_60_PSNR_1024",
        "dcvc_quality": 3
    }
}

# -------------------------
# Frame selection
# RLVC frames are 1-indexed (f001.png, f002.png ...)
# DCVC frames are 0-indexed (recon_frame_0.png ...)
# -------------------------
frame_rlvc_idx = 49
frame_rlvc = f"f{frame_rlvc_idx:03d}.png"
frame_dcvc_idx = frame_rlvc_idx - 1

# -------------------------
# Process sequences
# -------------------------
for seq_name, seq_info in sequences.items():
    folder = seq_info["folder"]
    rlvc_lambda_folder = seq_info["rlvc_lambda_folder"]
    dcvc_quality = seq_info["dcvc_quality"]

    # RLVC path
    rlvc_img_path = os.path.join(rlvc_root, folder, rlvc_lambda_folder, "frames", frame_rlvc)
    # DCVC path
    dcvc_img_path = os.path.join(dcvc_root, folder, f"model_dcvc_quality_{dcvc_quality}_psnr", f"recon_frame_{frame_dcvc_idx}.png")

    # Check existence
    if not os.path.exists(rlvc_img_path):
        print(f"[RLVC] File not found: {rlvc_img_path}")
        continue
    if not os.path.exists(dcvc_img_path):
        print(f"[DCVC] File not found: {dcvc_img_path}")
        continue

    # --- Step 1: select patch interactively on RLVC ---
    rlvc_img = cv2.imread(rlvc_img_path)
    print(f"Select patch for {seq_name} (RLVC)")
    r = cv2.selectROI(f"Select patch: {seq_name}", rlvc_img, showCrosshair=True, fromCenter=False)
    cv2.destroyAllWindows()
    x, y, w, h = r
    print(f"Selected patch: x={x}, y={y}, w={w}, h={h}")

    # --- Step 2: crop RLVC ---
    rlvc_cropped = rlvc_img[y:y+h, x:x+w]
    rlvc_save_path = os.path.join(output_root, f"{seq_name}_RLVC_f{frame_rlvc_idx:03d}_cropped.png")
    cv2.imwrite(rlvc_save_path, rlvc_cropped)

    # --- Step 3: crop DCVC with same coordinates ---
    dcvc_img = cv2.imread(dcvc_img_path)
    dcvc_cropped = dcvc_img[y:y+h, x:x+w]
    dcvc_save_path = os.path.join(output_root, f"{seq_name}_DCVC_f{frame_rlvc_idx:03d}_cropped.png")
    cv2.imwrite(dcvc_save_path, dcvc_cropped)

    print(f"Cropped images saved for {seq_name} in {output_root}")
