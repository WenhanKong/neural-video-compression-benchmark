import json
import csv
import pandas as pd
import os

def convert_and_combine():
    """
    Converts DCVC JSON results to a CSV file, then combines it with
    RLVC results, adding a 'Model' column to each.
    """
    # --- Part 1: Convert DCVC JSON files to a single CSV ---

    json_files = ['DCVC/DCVC_psnr_results.json', 'DCVC/DCVC_msssim_results.json']
    dcvc_csv_file = 'dcvc_results_converted.csv'
    
    print(f"Step 1: Converting DCVC JSON files to '{dcvc_csv_file}'...")

    try:
        with open(dcvc_csv_file, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Sequence', 'MetricType', 'Lambda', 'Metric', 'bpp'])

            for json_file in json_files:
                if not os.path.exists(json_file):
                    print(f"  ERROR: Source file '{json_file}' not found. Aborting.")
                    return

                metric_type = "PSNR" if "psnr" in json_file else "MS-SSIM"
                with open(json_file, 'r') as f:
                    data = json.load(f)
                    for dataset_name, sequences in data.items():
                        for sequence_name, models in sequences.items():
                            for model_name, metrics in models.items():
                                try:
                                    lambda_val = model_name.split('_')[3]
                                except IndexError:
                                    lambda_val = "N/A"
                                
                                metric_val = metrics.get('ave_all_frame_quality')
                                bpp_val = metrics.get('ave_all_frame_bpp')

                                if metric_val is not None and bpp_val is not None:
                                    csv_writer.writerow([sequence_name, metric_type, lambda_val, metric_val, bpp_val])
        print("  DCVC conversion successful.")

    except Exception as e:
        print(f"  An error occurred during JSON to CSV conversion: {e}")
        return

    # --- Part 2: Concatenate RLVC and DCVC CSVs ---
    
    final_csv_file = 'combined_results.csv'
    rlvc_csv_file = 'RLVC/RLVC_results.csv'

    print(f"\nStep 2: Combining results into '{final_csv_file}'...")
    
    if not os.path.exists(rlvc_csv_file):
        print(f"  ERROR: Source file '{rlvc_csv_file}' not found. Aborting.")
        return

    try:
        # Read both CSV files into pandas DataFrames
        rlvc_df = pd.read_csv(rlvc_csv_file)
        dcvc_df = pd.read_csv(dcvc_csv_file)

        # Add the 'Model' column to distinguish them
        rlvc_df['Model'] = 'RLVC'
        dcvc_df['Model'] = 'DCVC'

        # Concatenate the two DataFrames
        combined_df = pd.concat([rlvc_df, dcvc_df], ignore_index=True)

        # Save the final combined DataFrame to a new CSV
        combined_df.to_csv(final_csv_file, index=False)
        print(f"  Successfully combined files.")
        
    except Exception as e:
        print(f"  An error occurred during CSV concatenation: {e}")

if __name__ == '__main__':
    convert_and_combine()