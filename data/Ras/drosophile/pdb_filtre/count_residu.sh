#!/bin/bash

# Parcours de tous les fichiers PDB dans le dossier
for pdb_file in *.pdb; do
    # Utilisation de grep pour rechercher les lignes contenant les résidus dans le fichier PDB
    # et compter le nombre total de ces lignes
    residue_count=$(grep "^ATOM\|^HETATM" "$pdb_file" | grep -c " CA ")

    # Affichage du nombre total de résidus pour chaque fichier
    echo "Fichier : $pdb_file - Nombre total de résidus : $residue_count"
done


