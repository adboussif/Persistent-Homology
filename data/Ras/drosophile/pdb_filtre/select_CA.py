#!/usr/bin/env python3
import os

# Définition d'une fonction pour extraire les lignes des carbones alpha
def extract_alpha_carbons_lines(filename):
    alpha_carbons_lines = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                alpha_carbons_lines.append(line)
    return alpha_carbons_lines

# Répertoire contenant les fichiers PDB
pdb_directory = "/data/home/tfoussenisalamicisse/projet_hp/pdb_files_dosoph/pdb_files/pdb_filtre"

# Créer un dossier pour stocker les fichiers avec les lignes des carbones alpha
output_directory = "pdb_ca_files"
os.makedirs(output_directory, exist_ok=True)

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

