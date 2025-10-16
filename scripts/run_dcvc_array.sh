#!/bin/bash

#SBATCH --job-name=dcvc_array          # Job name
#SBATCH --cpus-per-task=4              # Number of CPU cores per task
#SBATCH --mem=64G                      # Job memory request
#SBATCH --time=24:00:00                # Time limit hrs:min:sec
#SBATCH --partition=gpu                # Partition name
#SBATCH --gres=gpu:1                   # Request 1 GPU
#SBATCH --array=0-1                    # Submit an array of 2 jobs (indexed 0 and 1)
#SBATCH --output=/WAVE/users2/unix/wkong/compress396/project2/results/logs/%x_%A_%a.out

# --- Job Configuration using Bash Arrays ---
# Each index (0, 1, etc.) corresponds to a job in the array.

# Array of metrics to test (psnr, msssim)
MODEL_TYPES=("psnr" "msssim")

# Array of I-frame model architectures
IFRAME_MODEL_NAMES=("cheng2020-anchor" "bmshj2018-hyperprior")

# Array of I-frame model paths (each element is a single string)
IFRAME_PATHS=(
  "checkpoints/cheng2020-anchor-3-e49be189.pth.tar checkpoints/cheng2020-anchor-4-98b0b468.pth.tar checkpoints/cheng2020-anchor-5-23852949.pth.tar checkpoints/cheng2020-anchor-6-4c052b1a.pth.tar"
  "checkpoints/bmshj2018-hyperprior-ms-ssim-3-92dd7878.pth.tar checkpoints/bmshj2018-hyperprior-ms-ssim-4-4377354e.pth.tar checkpoints/bmshj2018-hyperprior-ms-ssim-5-c34afc8d.pth.tar checkpoints/bmshj2018-hyperprior-ms-ssim-6-3a6d8229.pth.tar"
)

# Array of main DCVC model paths (each element is a single string)
MODEL_PATHS=(
  "checkpoints/model_dcvc_quality_0_psnr.pth checkpoints/model_dcvc_quality_1_psnr.pth checkpoints/model_dcvc_quality_2_psnr.pth checkpoints/model_dcvc_quality_3_psnr.pth"
  "checkpoints/model_dcvc_quality_0_msssim.pth checkpoints/model_dcvc_quality_1_msssim.pth checkpoints/model_dcvc_quality_2_msssim.pth checkpoints/model_dcvc_quality_3_msssim.pth"
)

# Array of output filenames
OUTPUT_FILES=("/WAVE/users2/unix/wkong/compress396/project2/results/DCVC_psnr_results.json" "/WAVE/users2/unix/wkong/compress396/project2/results/DCVC_msssim_results.json")
RECON_PATHS=("/WAVE/users2/unix/wkong/compress396/project2/results/reconstructed_frames_psnr" "/WAVE/users2/unix/wkong/compress396/project2/results/reconstructed_frames_msssim")

# --- Select Parameters based on Array Task ID ---
TASK_ID=$SLURM_ARRAY_TASK_ID
CURRENT_MODEL_TYPE=${MODEL_TYPES[$TASK_ID]}
CURRENT_IFRAME_NAME=${IFRAME_MODEL_NAMES[$TASK_ID]}
CURRENT_IFRAME_PATH=${IFRAME_PATHS[$TASK_ID]}
CURRENT_MODEL_PATH=${MODEL_PATHS[$TASK_ID]}
CURRENT_OUTPUT_FILE=${OUTPUT_FILES[$TASK_ID]}
CURRENT_RECON_PATH=${RECON_PATHS[$TASK_ID]}

# --- Environment Setup ---
echo "Starting Job: ${CURRENT_MODEL_TYPE} test (Task ID: $TASK_ID)"
module load CUDA
source ~/miniconda3/etc/profile.d/conda.sh
conda activate dcvc

cd /WAVE/users2/unix/wkong/compress396/project2/code/DCVC/DCVC-family/DCVC || exit 1
mkdir -p ${CURRENT_RECON_PATH}

# --- Execute the Test ---
# This command is now generic. The variables determine which test is run.
LOG_FILE="/WAVE/users2/unix/wkong/compress396/project2/results/logs/DCVC_${CURRENT_MODEL_TYPE}.out"
python test_video.py \
  --test_config my_test_config.json \
  --model_type ${CURRENT_MODEL_TYPE} \
  --i_frame_model_name ${CURRENT_IFRAME_NAME} \
  --i_frame_model_path ${CURRENT_IFRAME_PATH} \
  --model_path ${CURRENT_MODEL_PATH} \
  --output_json_result_path ${CURRENT_OUTPUT_FILE} \
  --cuda True --cuda_device 0 --worker 1 \
  --write_recon_frame True \
  --recon_bin_path ${CURRENT_RECON_PATH} \
  >> "$LOG_FILE" 2>&1
  
echo "Job with Task ID $TASK_ID finished."