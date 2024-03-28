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
        for line in file:
            if line.startswith("ATOM") and " CA " in line:
                count += 1
    return count

def calculate_normalized_wasserstein_distance(args):
    file1, file2, pdb_a_dir, pdb_b_dir = args
    df1 = pd.read_csv(file1, usecols=["Birth", "Death"]).dropna().to_numpy()
    df2 = pd.read_csv(file2, usecols=["Birth", "Death"]).dropna().to_numpy()

    if df1.size == 0 or df2.size == 0:
        return np.nan, file1, file2, 0, 0  # Retourne 0 pour les nombres de carbones si df vide

    pdb_file1 = os.path.join(pdb_a_dir, os.path.basename(file1).replace('_barcodes.csv', '.pdb'))
    pdb_file2 = os.path.join(pdb_b_dir, os.path.basename(file2).replace('_barcodes.csv', '.pdb'))

    count1 = count_alpha_carbons(pdb_file1)
    count2 = count_alpha_carbons(pdb_file2)

    mean_alpha_count = (count1 + count2) / 2.0

    if mean_alpha_count == 0:
        return np.nan, file1, file2, count1, count2

    distance = wasserstein_distance(df1, df2, order=1.0, internal_p=2.0,keep_essential_parts=False)
    normalized_distance = distance / mean_alpha_count

    return normalized_distance, file1, file2, count1, count2

def process_pairs(csv_a_dir, pdb_a_dir, csv_b_dir, pdb_b_dir):
    tasks = []
    for file_a in os.listdir(csv_a_dir):
        if file_a.endswith('_barcodes.csv'):
            barcode_file_a = os.path.join(csv_a_dir, file_a)
            for file_b in os.listdir(csv_b_dir):
                if file_b.endswith('_barcodes.csv'):
                    barcode_file_b = os.path.join(csv_b_dir, file_b)
                    tasks.append((barcode_file_a, barcode_file_b, pdb_a_dir, pdb_b_dir))

    with multiprocessing.Pool() as pool:
        results = pool.map(calculate_normalized_wasserstein_distance, tasks)

    return results

def visualize_results(distances, num_files_a, num_files_b, file_pairs, target_files, reference_files):
    distances = [result[0] for result in results if result[0] is not np.nan]
    num_files_a = len(set([os.path.basename(result[1]) for result in results]))
    num_files_b = len(set([os.path.basename(result[2]) for result in results]))

    # Création de la matrice de distance
    distance_matrix = np.full((num_files_a, num_files_b), np.nan)
    target_files = sorted(list(set([os.path.basename(result[1]).replace('_barcodes.csv', '') for result in results])))
    reference_files = sorted(list(set([os.path.basename(result[2]).replace('_barcodes.csv', '') for result in results])))

    for result in results:
        if not np.isnan(result[0]):
            row = target_files.index(os.path.basename(result[1]).replace('_barcodes.csv', ''))
            col = reference_files.index(os.path.basename(result[2]).replace('_barcodes.csv', ''))
            distance_matrix[row, col] = result[0]

    # Visualisation
    fig, axs = plt.subplots(1, 2, figsize=(14, 7))
    sns.kdeplot(distances, ax=axs[0], fill=True)
    axs[0].set_title('Graphique de densité des Distances de Wasserstein')
    axs[0].set_xlabel('Distance')
    axs[0].set_ylabel('Densité')
    median = np.median(distances)
    q1 = np.percentile(distances, 25)
    q3 = np.percentile(distances, 75)
    axs[0].axvline(median, color='r', linestyle='--', label=f'Médiane: {median:.2f}')
    axs[0].axvline(q1, color='g', linestyle='--', label=f'Q1: {q1:.3f}')
    axs[0].axvline(q3, color='b', linestyle='--', label=f'Q3: {q3:.3f}')
    axs[0].legend()

    # Tracé de la heatmap
    im = axs[1].imshow(distance_matrix, cmap='viridis', aspect='auto')
    fig.colorbar(im, ax=axs[1])
    axs[1].set_title('Heatmap des distances de Wasserstein')
    axs[1].set_xlabel('bcl')
    axs[1].set_ylabel('zebra_fish')

    # Optionnel: Ajuster les étiquettes des axes si vous avez les listes de noms
    # axs[1].set_xticks(np.arange(len(reference_files)))
    # axs[1].set_yticks(np.arange(len(target_files)))
    # axs[1].set_xticklabels(reference_files)
    # axs[1].set_yticklabels(target_files)
    # plt.setp(axs[1].get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    plt.tight_layout()
    plt.savefig('bcl_zebrafish_visualization.png')
    plt.close(fig)
def save_results_to_csv(results, output_csv_path="output_distances.csv"):
    # Sorting the results based on the normalized distances
    sorted_results = sorted(results, key=lambda x: x[0] if x[0] is not np.nan else np.inf)

    # Preparing the data for the DataFrame
    data = [[os.path.basename(r[1]).replace('_barcodes.csv', ''),
             os.path.basename(r[2]).replace('_barcodes.csv', ''),
             r[0], r[3], r[4]] for r in sorted_results if r[0] is not np.nan]

    # Creating DataFrame and saving to CSV
    df = pd.DataFrame(data, columns=['Barcode homo zebra_fish', 'Barcode bcl', 'Distance',
                                     'Nb Carbone Alpha zebra_fish', 'Nb Carbone Alpha bcl'])
    df.to_csv(output_csv_path, index=False)

if __name__ == "__main__":
    csv_a_dir = "/data/home/tfoussenisalamicisse/projet_hp/pdb_files_zebrafish/bc_dim1"
    pdb_a_dir = "/data/home/tfoussenisalamicisse/projet_hp/pdb_files_zebrafish/pdb_ca_files"
    csv_b_dir = "/data/home/tfoussenisalamicisse/projet_hp/results/bc_dim1"
    pdb_b_dir = "/data/home/tfoussenisalamicisse/projet_hp/all_prot_structure_coord"

    # Processing pairs and obtaining results
    results = process_pairs(csv_a_dir, pdb_a_dir, csv_b_dir, pdb_b_dir)

    # Extracting unique file names for targets and references from results for the heatmap labels
    target_files = list(set([os.path.basename(result[1]).replace('_barcodes.csv', '') for result in results]))
    reference_files = list(set([os.path.basename(result[2]).replace('_barcodes.csv', '') for result in results]))
    num_files_a = len(target_files)
    num_files_b = len(reference_files)


    visualize_results([res[0] for res in results], num_files_a, num_files_b,
                      [(res[1], res[2]) for res in results], target_files, reference_files)

    # Saving results to CSV
    save_results_to_csv(results)

