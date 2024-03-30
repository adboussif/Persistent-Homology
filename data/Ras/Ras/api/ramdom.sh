#!/bin/bash

# Chemin du dossier contenant les fichiers PDB originaux
SOURCE_DIR="/data/home/aboussif/Projet14/deliverable/topologie/data/Ras/Ras/pdb"

# Chemin du dossier de destination pour les 100 fichiers PDB sélectionnés
DEST_DIR="/data/home/aboussif/Projet14/deliverable/topologie/data/Ras/Ras/pdb_files"

# Créer le dossier de destination s'il n'existe pas
mkdir -p "$DEST_DIR"

# Sélectionner aléatoirement 100 fichiers PDB et les copier dans le dossier de destination
find "$SOURCE_DIR" -name '*.pdb' | shuf -n 100 | xargs -I {} cp {} "$DEST_DIR"
