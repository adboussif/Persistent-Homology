#!/usr/bin/env python3
import os
import argparse

# Configurer le parseur d'arguments
parser = argparse.ArgumentParser(description="Extract alpha carbon lines from PDB files.")
parser.add_argument("-d", "--pdb_dir", required=True, help="Path to the directory containing PDB files.")
parser.add_argument("-o", "--output_dir", required=True, help="Path to the output directory for extracted alpha carbon files.")

# Parser les arguments
args = parser.parse_args()

# Définition d'une fonction pour extraire les lignes des carbones alpha
def extract_alpha_carbons_lines(filename):
    alpha_carbons_lines = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                alpha_carbons_lines.append(line)
    return alpha_carbons_lines

# Répertoire contenant les fichiers PDB, spécifié par l'utilisateur
pdb_directory = args.pdb_dir

# Créer un dossier pour stocker les fichiers avec les lignes des carbones alpha, spécifié par l'utilisateur
output_directory = args.output_dir
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Parcourir tous les fichiers dans le répertoire spécifié
for filename in os.listdir(pdb_directory):
    if filename.endswith(".pdb"):
        # Chemin complet du fichier d'entrée
        input_file_path = os.path.join(pdb_directory, filename)

        # Extraire les lignes des carbones alpha
        alpha_carbons_lines = extract_alpha_carbons_lines(input_file_path)

        # Chemin de sortie pour stocker les résultats
        output_file_path = os.path.join(output_directory, os.path.splitext(filename)[0] + "_ca.pdb")

        # Écrire les lignes des carbones alpha dans le fichier de sortie
        with open(output_file_path, 'w') as output_file:
            for line in alpha_carbons_lines:
                output_file.write(line)
