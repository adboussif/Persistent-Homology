#!/usr/bin/env python3

import argparse
import os
from functools import partial
from alpha import explore_and_process_files, process_file
from analyse import process_pairs, visualize_results, save_results_to_csv

def main(reference_path, target_path, output_dir):
    # Configuration des dossiers pour les barcodes et les fichiers CSV pour la référence et la cible
    base_dir_ref = os.path.join(output_dir, "reference")
    base_dir_target = os.path.join(output_dir, "target")

    # Création des dossiers de base nécessaires
    os.makedirs(base_dir_ref, exist_ok=True)
    os.makedirs(base_dir_target, exist_ok=True)

    # Génération des barcodes pour les fichiers PDB de référence et cible
    explore_and_process_files(reference_path, base_dir_ref, partial(process_file, output_dir=base_dir_ref, dimension='1', is_reference=True))
    explore_and_process_files(target_path, base_dir_target, partial(process_file, output_dir=base_dir_target, dimension='2', is_reference=False))

    # Traitement des distances et visualisation pour chaque type de barcode
    for barcode_suffix in ['1', '2']:
        print(f"Traitement des distances pour barcode{barcode_suffix}.")
        results = process_pairs(os.path.join(base_dir_ref, "output"), 
                        barcode_suffix, 
                        reference_path, 
                        target_path)
        visualize_results(results, barcode_suffix, output_dir)

    # Enregistrement des résultats globaux dans un fichier CSV
    save_results_to_csv_path = os.path.join(output_dir, "distance_results.csv")
    save_results_to_csv(results, save_results_to_csv_path, barcode_suffix)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script pour l'analyse topologique des protéines.")
    parser.add_argument('-ref', '--reference', required=True, help="Chemin vers le dossier contenant les fichiers PDB de référence.")
    parser.add_argument('-target', '--target', required=True, help="Chemin vers le dossier contenant les fichiers PDB cibles.")
    parser.add_argument('-o', '--output', required=True, help="Chemin vers le dossier où sauvegarder les résultats.")
    
    args = parser.parse_args()
    main(args.reference, args.target, args.output)
