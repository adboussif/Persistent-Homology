#!/usr/bin/env python3

from gudhi.wasserstein import wasserstein_distance
import numpy as np
import os
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import multiprocessing

def count_alpha_carbons(file_path):
    count = 0
    with open(file_path, 'r') as file:
        for line in file.readlines():
            if line.startswith("ATOM") and " CA " in line:
                count += 1
    return count

def calculate_normalized_wasserstein_distance(args):
    ref_file, target_file, ref_output_csv_dir, pdb_file1_path, pdb_file2_path = args
    df1 = pd.read_csv(os.path.join(ref_output_csv_dir, ref_file), usecols=["Birth", "Death"]).dropna().to_numpy()
    df2 = pd.read_csv(os.path.join(ref_output_csv_dir, target_file), usecols=["Birth", "Death"]).dropna().to_numpy()

    if df1.size == 0 or df2.size == 0:
        return np.nan, ref_file, target_file, 0, 0

    count1 = count_alpha_carbons(pdb_file1_path)
    count2 = count_alpha_carbons(pdb_file2_path)
    mean_alpha_count = (count1 + count2) / 2.0

    if mean_alpha_count == 0:
        return np.nan, ref_file, target_file, count1, count2

    distance = wasserstein_distance(df1, df2, order=1, internal_p=2)
    normalized_distance = distance / mean_alpha_count

    return normalized_distance, ref_file, target_file, count1, count2

    print("Distances calculées")

def construct_pdb_path(file_name, pdb_reference_dir, pdb_target_dir):
    actual_file_name = file_name.replace('ref_', '').replace('target_', '').replace('_barcode1.csv', '.pdb').replace('_barcode2.csv', '.pdb')
    if 'ref_' in file_name:
        return os.path.join(pdb_reference_dir, actual_file_name)
    else:
        return os.path.join(pdb_target_dir, actual_file_name)



def process_pairs(ref_output_csv_dir, target_output_csv_dir, barcode_suffix, pdb_reference_dir, pdb_target_dir):
    ref_files = [f for f in os.listdir(ref_output_csv_dir) if f.startswith('ref_') and f.endswith(f'_barcode{barcode_suffix}.csv')]
    target_files = [f for f in os.listdir(target_output_csv_dir) if f.startswith('target_') and f.endswith(f'_barcode{barcode_suffix}.csv')]

    tasks = []
    for ref_file in ref_files:
        for target_file in target_files:
            pdb_file1_path = construct_pdb_path(ref_file, pdb_reference_dir, pdb_target_dir)
            pdb_file2_path = construct_pdb_path(target_file, pdb_reference_dir, pdb_target_dir)
            tasks.append((ref_file, target_file, ref_output_csv_dir, pdb_file1_path, pdb_file2_path))

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
    axs[0].set_title(f'Graphe de densité des Distances en Dimension {barcode_suffix}')
    axs[0].set_xlabel('Distance')
    axs[0].set_ylabel('Densité')

    median, q1, q3 = np.median(distances), np.percentile(distances, 25), np.percentile(distances, 75)
    axs[0].axvline(median, color='r', linestyle='--', label=f'Médiane: {median:.3f}')
    axs[0].axvline(q1, color='g', linestyle='--', label=f'Q1: {q1:.3f}')
    axs[0].axvline(q3, color='b', linestyle='--', label=f'Q3: {q3:.3f}')
    axs[0].legend()

    im = axs[1].imshow(distance_matrix, cmap='viridis', aspect='auto')
    fig.colorbar(im, ax=axs[1])
    axs[1].set_title(f'Heatmap of Wasserstein Distances - Barcode {barcode_suffix}')
    axs[1].set_xlabel('Reference')
    axs[1].set_ylabel('Target')

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

