#!/usr/bin/env python3

from gudhi.wasserstein import wasserstein_distance
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import multiprocessing

def count_alpha_carbons(file_path):
    """Compte le nombre de carbones alpha dans un fichier PDB donné."""
    count = 0
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if line.startswith("ATOM") and " CA " in line:
                count += 1
    return count

def calculate_normalized_wasserstein_distance(args):
    file1, file2, output_csv_dir, pdb_reference_dir, pdb_target_dir = args
    df1 = pd.read_csv(os.path.join(output_csv_dir, file1), usecols=["Birth", "Death"]).dropna().to_numpy()
    df2 = pd.read_csv(os.path.join(output_csv_dir, file2), usecols=["Birth", "Death"]).dropna().to_numpy()

    if df1.size == 0 or df2.size == 0:
        return np.nan, file1, file2, 0, 0

    pdb_file1 = os.path.join(pdb_reference_dir, file1.replace('_barcode1.csv', '.pdb').replace('_barcode2.csv', '.pdb'))
    pdb_file2 = os.path.join(pdb_target_dir, file2.replace('_barcode1.csv', '.pdb').replace('_barcode2.csv', '.pdb'))
    
    count1 = count_alpha_carbons(pdb_file1)
    count2 = count_alpha_carbons(pdb_file2)
    mean_alpha_count = (count1 + count2) / 2.0

    if mean_alpha_count == 0:
        return np.nan, file1, file2, count1, count2

    distance = wasserstein_distance(df1, df2, order=1, internal_p=2)
    normalized_distance = distance / mean_alpha_count

    return normalized_distance, file1, file2, count1, count2

def process_pairs(output_csv_dir, barcode_suffix, pdb_reference_dir, pdb_target_dir):
    tasks = []
    for file_a in os.listdir(output_csv_dir):
        if file_a.endswith(f'_barcode{barcode_suffix}.csv'):
            for file_b in os.listdir(output_csv_dir):
                if file_b.endswith(f'_barcode{barcode_suffix}.csv') and file_a != file_b:
                    tasks.append((file_a, file_b, output_csv_dir, pdb_reference_dir, pdb_target_dir))

    with multiprocessing.Pool() as pool:
        results = pool.map(calculate_normalized_wasserstein_distance, tasks)

    return results

def visualize_results(results, barcode_suffix, output_dir):
    filtered_results = [result for result in results if f"_barcode{barcode_suffix}.csv" in result[1]]

    if not filtered_results:
        print(f"No valid distances found for visualization with barcode suffix '{barcode_suffix}'.")
        return

    distances = [res[0] for res in filtered_results if res[0] is not np.nan]
    if not distances:
        print("No valid distances for visualization.")
        return

    file_names = sorted(set(res[1] for res in filtered_results) | set(res[2] for res in filtered_results))
    file_index = {name: idx for idx, name in enumerate(file_names)}

    distance_matrix = np.full((len(file_names), len(file_names)), np.nan)
    for res in filtered_results:
        if res[0] is not np.nan:
            i = file_index[res[1]]
            j = file_index[res[2]]
            distance_matrix[i, j] = res[0]

    fig, axs = plt.subplots(1, 2, figsize=(14, 7))

    sns.kdeplot(distances, ax=axs[0], fill=True)
    axs[0].set_title(f'Density Plot of Wasserstein Distances - Barcode {barcode_suffix}')
    axs[0].set_xlabel('Distance')
    axs[0].set_ylabel('Density')

    median, q1, q3 = np.median(distances), np.percentile(distances, 25), np.percentile(distances, 75)
    axs[0].axvline(median, color='r', linestyle='--', label=f'Médiane: {median:.3f}')
    axs[0].axvline(q1, color='g', linestyle='--', label=f'Q1: {q1:.3f}')
    axs[0].axvline(q3, color='b', linestyle='--', label=f'Q3: {q3:.3f}')
    axs[0].legend()

    im = axs[1].imshow(distance_matrix, cmap='viridis', aspect='auto')
    fig.colorbar(im, ax=axs[1])
    axs[1].set_title(f'Heatmap of Wasserstein Distances - Barcode {barcode_suffix}')
    axs[1].set_xlabel('Files')
    axs[1].set_ylabel('Files')

    axs[1].set_xticks([])
    axs[1].set_yticks([])

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'visualization_barcode{barcode_suffix}.png'))
    plt.close(fig)


def save_results_to_csv(results, output_csv_path, barcode_suffix):
    filtered_results = [result for result in results if f"_barcode{barcode_suffix}.csv" in result[1]]
    sorted_results = sorted(filtered_results, key=lambda x: x[0] if x[0] is not np.nan else np.inf)

    data = [
        [
            os.path.basename(r[1]).replace(f'_barcode{barcode_suffix}.csv', ''),
            os.path.basename(r[2]).replace(f'_barcode{barcode_suffix}.csv', ''),
            r[0], r[3], r[4]
        ] 
        for r in sorted_results if r[0] is not np.nan
    ]

    df = pd.DataFrame(data, columns=['Target Barcode', 'Reference Barcode', 'Distance', 'Number of Alpha Carbons in Target', 'Number of Alpha Carbons in Reference'])
    adjusted_output_csv_path = output_csv_path.replace('.csv', f'_barcode{barcode_suffix}.csv')
    df.to_csv(adjusted_output_csv_path, index=False)

    print(f"Results saved to {adjusted_output_csv_path}.")
