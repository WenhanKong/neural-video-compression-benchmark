#!/bin/bash
#SBATCH --job-name=rlvc_batch
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=4              # Number of CPU cores per task
#SBATCH --mem=64G
#SBATCH --time=24:00:00
#SBATCH --array=0
#SBATCH --output=/WAVE/users2/unix/wkong/compress396/project2/results/logs/%x_%A_%a.out

# ---- PATHS ----
DATA_ROOT="/WAVE/users2/unix/wkong/compress396/project2/datasets"
RESULT_ROOT="/WAVE/users2/unix/wkong/compress396/project2/results"
SCRIPT_PATH="/WAVE/users2/unix/wkong/compress396/project2/code/RLVC/RLVC.py"

# ---- SEQUENCES ----
sequences=(
# "$DATA_ROOT/ClassB-1920x1080/BQTerrace_1920x1072_60"
# "$DATA_ROOT/ClassB-1920x1080/BasketballDrive_1920x1072_50"
# "$DATA_ROOT/ClassC-832x480/PartyScene_832x480_50"
# "$DATA_ROOT/ClassC-832x480/RaceHorses_832x480_30"
# "$DATA_ROOT/ClassD-416x240/BQSquare_416x240_60"
"/WAVE/users2/unix/wkong/compress396/project2/datasets/ClassD-416x240/BlowingBubbles_416x240_50"
# "$DATA_ROOT/ClassE-1280x720/Johnny_1280x720_60"
# "$DATA_ROOT/ClassE-1280x720/KristenAndSara_1280x720_60"
)

# ---- ENV ----
SEQ_PATH="${sequences[$SLURM_ARRAY_TASK_ID]}"
SEQ_NAME=$(basename "$SEQ_PATH")
mkdir -p "$RESULT_ROOT/logs"

# Add BPG tools to PATH
export PATH=/WAVE/users2/unix/wkong/libbpg-0.9.8:$PATH

module load CUDA
source ~/miniconda3/etc/profile.d/conda.sh
conda activate rlvc

cd "/WAVE/users2/unix/wkong/compress396/project2/code/RLVC" || exit 1

# ---- PARAMETERS ----
# For a 100-frame video sequence (assuming frames are numbered starting from 1), the I-frames will be: 1, 14, 27, 40, 53, 66, 79, and 92
MODES=("MS-SSIM" "PSNR")
# MODES=("PSNR")
F_P=6
B_P=6
FRAME=100
PYTHON_PATH="python3"
CA_MODEL_PATH="/WAVE/users2/unix/wkong/compress396/project2/code/RLVC/CA_EntropyModel_Test"
ENTROPY_CODING=1

# ---- RUN ----
for MODE in "${MODES[@]}"; do
    if [ "$MODE" == "MS-SSIM" ]; then
        LAMBDAS=(8 16 32 64)
    else
        LAMBDAS=(256 512 1024 2048)
    fi

    for LAMBDA in "${LAMBDAS[@]}"; do
        LOG_FILE="$RESULT_ROOT/logs/RLVC_${SEQ_NAME}_${MODE}_lambda${LAMBDA}.out"
        echo "[$(date)] Running ${SEQ_NAME} mode=${MODE} lambda=${LAMBDA}" > "$LOG_FILE"

        $PYTHON_PATH "$SCRIPT_PATH" \
            --path "$SEQ_PATH" \
            --frame "$FRAME" \
            --f_P "$F_P" \
            --b_P "$B_P" \
            --mode "$MODE" \
            --metric "$MODE" \
            --python_path "$PYTHON_PATH" \
            --CA_model_path "$CA_MODEL_PATH" \
            --l "$LAMBDA" \
            --entropy_coding "$ENTROPY_CODING" # >> "$LOG_FILE" 2>&1
    done
done

wait
echo "[$(date)] All configs done for ${SEQ_NAME}" >> "$RESULT_ROOT/logs/${SEQ_NAME}_done.log"
