
# %%
import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("combined_results.csv")

# Remove rows with missing bpp or Metric
df = df.dropna(subset=["bpp", "Metric"])

df_psnr = df[df["MetricType"] == "PSNR"]

# --- Group by model and compression setting ---
# Average across sequences for the same model and Lambda/quality
grouped = df_psnr.groupby(["Model", "Lambda"], as_index=False).agg({
    "bpp": "mean",
    "Metric": "mean"
})

# --- Plotting ---
plt.figure(figsize=(8,5))

for model_name in grouped["Model"].unique():
    model_df = grouped[grouped["Model"] == model_name].sort_values("bpp")
    plt.plot(model_df["bpp"], model_df["Metric"], marker='o', label=model_name)

plt.xlabel("bpp")
plt.ylabel("PSNR (dB)")
plt.title("RD Curve: PSNR vs bpp")
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()


# %%
df_msssim = df[df["MetricType"] == "MS-SSIM"]

# --- Group by model and compression setting ---
# Average across sequences for the same model and Lambda/quality
grouped = df_msssim.groupby(["Model", "Lambda"], as_index=False).agg({
    "bpp": "mean",
    "Metric": "mean"
})

# --- Plotting ---
plt.figure(figsize=(8,5))

for model_name in grouped["Model"].unique():
    model_df = grouped[grouped["Model"] == model_name].sort_values("bpp")
    plt.plot(model_df["bpp"], model_df["Metric"], marker='o', label=model_name)

plt.xlabel("bpp")
plt.ylabel("MS-SSIM")
plt.title("RD Curve: MS-SSIM vs bpp")
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend()
plt.tight_layout()
plt.show()

# %%
