import pickle
import numpy as np
import os
import csv
import argparse

# Configurer le parseur d'arguments
parser = argparse.ArgumentParser(description="Process PDB files based on pLDDT scores.")
parser.add_argument("-d", "--pdb_dir", required=True, help="Path to the directory containing PDB files.")
parser.add_argument("-o", "--output_dir", required=True, help="Path to the output directory.")

# Parser les arguments
args = parser.parse_args()

# Assigner les chemins à partir des arguments
root_path = args.pdb_dir
confiance_path = args.output_dir

# Seuil pour le score pLDDT
seuil_pLDDT = 70

# Pourcentage maximal d'atomes Ca de faible confiance
max_faible_confiance_pct = 10

# Vérifier l'existence du dossier de sortie et le créer si nécessaire
if not os.path.exists(confiance_path):
    os.makedirs(confiance_path)

# Initialiser le fichier CSV de résumé
resume_csv_path = os.path.join(confiance_path, 'resume_confiance.csv')
with open(resume_csv_path, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Écrire l'en-tête du fichier CSV
    csvwriter.writerow(['Identifiant', 'Ca initial', 'Ca enlevé', 'pLDDT initial', 'pLDDT final'])

def creer_pdb_filtre_et_copier(pkl_file, pdb_file, subdir_name):
    # Charger les données depuis le fichier pickle
    with open(pkl_file, 'rb') as f:
        result_data = pickle.load(f)
    plddt_scores = result_data['plddt']
    
    # Lire le fichier PDB
    with open(pdb_file, 'r') as pdb:
        lines = pdb.readlines()
    
    # Filtrer les lignes contenant les atomes CA
    ca_lines = [line for line in lines if line.startswith("ATOM") and " CA " in line]
    nombre_initial_ca = len(ca_lines)
    plddt_moyen_initial = np.mean([plddt_scores[int(line[22:26].strip()) - 1] for line in ca_lines])
    
    # Calculer le pourcentage d'atomes CA de faible confiance
    ca_faible_confiance = sum(plddt_scores[int(line[22:26].strip()) - 1] < seuil_pLDDT for line in ca_lines)
    pct_faible_confiance = (ca_faible_confiance / nombre_initial_ca) * 100
    
    suffixe_dossier = "_all_Ca" if pct_faible_confiance <= max_faible_confiance_pct else "_filtered_Ca"
    confiance_subdir_name = f"{subdir_name}{suffixe_dossier}"
    confiance_subdir_path = os.path.join(confiance_path, confiance_subdir_name)
    
    # Créer le sous-dossier si nécessaire
    if not os.path.exists(confiance_subdir_path):
        os.makedirs(confiance_subdir_path)
    
    # Chemin du fichier PDB filtré
    pdb_filtre_nom = f"{subdir_name}{suffixe_dossier}.pdb"
    pdb_filtre_path = os.path.join(confiance_subdir_path, pdb_filtre_nom)
    
    # Filtrer les atomes CA basés sur le score pLDDT
    ca_filtres = ca_lines if suffixe_dossier == "_all_Ca" else [line for line in ca_lines if plddt_scores[int(line[22:26].strip()) - 1] >= seuil_pLDDT]
    
    # Écrire le fichier PDB filtré
    with open(pdb_filtre_path, 'w') as pdb_filtre:
        pdb_filtre.writelines(ca_filtres)
    
    # Calculer les statistiques finales
    nombre_final_ca = len(ca_filtres)
    ca_enleves = nombre_initial_ca - nombre_final_ca
    plddt_moyen_final = np.mean([plddt_scores[int(line[22:26].strip()) - 1] for line in ca_filtres]) if nombre_final_ca > 0 else 0
    
    # Ajouter les données au fichier CSV
    with open(resume_csv_path, 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow([subdir_name, nombre_initial_ca, ca_enleves, plddt_moyen_initial, plddt_moyen_final])

# Traitement principal : parcourir tous les sous-dossiers dans le chemin spécifié
for subdir in os.listdir(root_path):
    subdir_path = os.path.join(root_path, subdir)
    if os.path.isdir(subdir_path):
        # Chemin vers les fichiers spécifiques attendus dans chaque sous-dossier
        pkl_file = os.path.join(subdir_path, 'result_model_1_pred_0.pkl')
        pdb_file = os.path.join(subdir_path, 'ranked_0.pdb')
        
        # Vérifier l'existence des fichiers nécessaires avant de procéder
        if os.path.exists(pkl_file) and os.path.exists(pdb_file):
            creer_pdb_filtre_et_copier(pkl_file, pdb_file, subdir)
            print(f"Traitement effectué pour la structure : {subdir}")
        else:
            print(f"Fichier(s) nécessaire(s) non trouvé(s) pour {subdir}")

