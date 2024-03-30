#!/usr/bin/env python3

import os
import argparse
import pandas as pd

def get_pdb_ids(pdb_dir):
    """Récupère les identifiants PDB à partir des noms de fichiers dans un répertoire."""
    pdb_ids = []
    for filename in os.listdir(pdb_dir):
        if filename.endswith(".pdb"):
            pdb_id = filename[:-4]  # Enlever '.pdb'
            pdb_ids.append(pdb_id)
    return pdb_ids

def get_function_from_pdb_file(pdb_file_path):
    with open(pdb_file_path, 'r') as file:
        for line in file:
            if line.startswith("HEADER"):
                # Divise la ligne en utilisant l'ID de la protéine comme délimiteur
                parts = line.split()  # Découpe la ligne en parties basées sur les espaces
                if len(parts) > 3:  # Vérifie qu'il y a suffisamment de parties
                    # La description de la fonction est entre 'HEADER' et l'ID de la protéine
                    function_description = " ".join(parts[1:-2]).strip()
                    return function_description
                break  # Sort de la boucle après avoir traité la ligne HEADER
    return "Function not found"


def create_annotation_dataframe(pdb_dir, pdb_ids):
    """Crée un DataFrame avec l'ID PDB et la fonction associée pour chaque fichier."""
    data = []
    for pdb_id in pdb_ids:
        pdb_file_path = os.path.join(pdb_dir, pdb_id + '.pdb')
        function = get_function_from_pdb_file(pdb_file_path)
        data.append([pdb_id, function])
    df = pd.DataFrame(data, columns=['PDB_ID', 'Function'])
    return df

def main(pdb_dir):
    pdb_ids = get_pdb_ids(pdb_dir)
    df = create_annotation_dataframe(pdb_dir, pdb_ids)
    output_csv_path = os.path.join(pdb_dir, "results_annotation.csv")
    df.to_csv(output_csv_path, index=False)
    print(f"Results saved to {output_csv_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script pour extraire des informations à partir des fichiers PDB et créer un fichier d'annotation.")
    parser.add_argument('-p', '--pdb', required=True, help="Chemin vers le dossier contenant les fichiers PDB.")
    args = parser.parse_args()
    main(args.pdb)
