#!/usr/bin/env python3
#!/usr/bin/env python3
import os
import csv

# Définition d'une fonction pour extraire les coordonnées des carbones alpha
def extract_alpha_carbons(filename):
    alpha_carbons = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                alpha_carbons.append((x, y, z))
    return alpha_carbons

# Chemin du répertoire contenant les fichiers PDB
input_dir = "/data/home/tfoussenisalamicisse/projet_hp/pdb_files_dosoph/pdb_files/pdb_filtre/pdb_ca_files/pdb_ca_files1"

# Chemin du dossier de sortie
output_dir = "/data/home/tfoussenisalamicisse/projet_hp/pdb_files_dosoph/ca_coord_files_csv"

# Parcourir tous les fichiers PDB dans le répertoire d'entrée
for file_name in os.listdir(input_dir):
    if file_name.endswith(".pdb"):
        # Chemin complet du fichier PDB d'entrée
        pdb_file_path = os.path.join(input_dir, file_name)
        
        # Extraire les coordonnées des carbones alpha
        alpha_carbons = extract_alpha_carbons(pdb_file_path)
        
        # Chemin de sortie pour le fichier CSV de coordonnées
        output_file = os.path.join(output_dir, f"{file_name[:-7]}_alpha_carbons.csv")

        # Écrire les coordonnées dans le fichier CSV de sortie
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(alpha_carbons)  # Écrire les coordonnées

