#!/usr/bin/env python3

import os
from Bio.PDB import PDBParser
import gudhi as gudhi
import matplotlib.pyplot as plt
import pandas as pd

def read_coordinates_from_pdb(file_path):
    parser = PDBParser()
    structure = parser.get_structure("protein", file_path)
    coordinates = []
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    coordinates.append(atom.get_coord())
    return coordinates

def calculate_alpha_complex(coordinates):
    alpha_complex = gudhi.AlphaComplex(points=coordinates)
    simplex_tree = alpha_complex.create_simplex_tree()
    simplex_tree.compute_persistence()
    barcode1 = simplex_tree.persistence_intervals_in_dimension(1)
    barcode2 = simplex_tree.persistence_intervals_in_dimension(2)
    return barcode1, barcode2

def process_file(input_path, output_dir, file_name, dimension):
    # Génération du chemin de base pour la sauvegarde des fichiers
    output_file_base = os.path.basename(file_name)[:-4]
    
    # Assure-toi que les chemins des dossiers pour les images et CSVs sont corrects
    barcode_image_dir = os.path.join(output_dir, 'barcodes')
    csv_output_dir = os.path.join(output_dir, 'output')

    # Vérifie et crée les dossiers si nécessaire
    os.makedirs(barcode_image_dir, exist_ok=True)
    os.makedirs(csv_output_dir, exist_ok=True)

    pdb_file_path = os.path.join(input_path, file_name)

    # Calcul des complexes alpha et des barcodes
    coordinates = read_coordinates_from_pdb(pdb_file_path)
    barcode1, barcode2 = calculate_alpha_complex(coordinates)

    # Sauvegarde des images de barcode
    for barcode, dim in zip([barcode1, barcode2], ['1', '2']):
        plt.figure(figsize=(8, 6))
        gudhi.plot_persistence_barcode(barcode)
        plt.title(f"Barcode{dim} for {output_file_base}")
        plt.xlabel("Birth")
        plt.ylabel("Death")
        plt.savefig(os.path.join(barcode_image_dir, f"{output_file_base}_barcode{dim}.png"))
        plt.close()

    # Sauvegarde des fichiers CSV des barcodes
    for barcode, dim in zip([barcode1, barcode2], ['1', '2']):
        barcode_df = pd.DataFrame(barcode, columns=["Birth", "Death"])
        csv_file_path = os.path.join(csv_output_dir, f"{output_file_base}_barcode{dim}.csv")
        barcode_df.to_csv(csv_file_path, index=False)


def explore_and_process_files(input_path, output_dir, process_file_callback):
    for root, _, files in os.walk(input_path):
        for file in files:
            if file.endswith('.pdb'):
                full_path = os.path.join(root, file)
                process_file_callback(input_path=root, output_dir=output_dir, file_name=file)
