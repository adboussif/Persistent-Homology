#!/bin/bash

# Définir le dossier source contenant les fichiers PDB
SOURCE_DIR="/data/home/aboussif/Projet14/deliverable/topologie/data/Ras/sapiens/pdb_filtre"

# Définir le dossier de destination pour les fichiers extraits
DEST_DIR="/data/home/aboussif/Projet14/deliverable/topologie/data/Ras/sapiens/pdb_files"

# Liste des identifiants PDB à extraire (basés sur les 4 premiers caractères)
pdb_ids=("5SGM" "6TFW" "6XI4" "7JHD" "7O08" "7ULU" "8BOK" "8G8S" "8SO1" "6GWQ" "6TWA" "6XJN" "7JO7" "7O3S" "7WCW" "8BS5" "8GM5" "8SWE" "6JVR" "6UJO" "6YUY" "7JQG" "7PRX" "7XHK" "8CIH" "8HAQ" "8UQB" "6KOJ" "6ULV" "6YYK" "7JVO" "7PWT" "7XUB" "8D6D" "8HTC" "8X72" "6KQP" "6UPR" "6ZUW" "7K2R" "7QG1" "7XVX" "8D6F" "8IIZ" "6LTK" "6VFQ" "7AXF" "7KHG" "7R3O" "7Y8D" "8DHH" "8K71" "6LXC" "6VNV" "7AZW" "7KP1" "7R5F" "7Y9C" "8E8B" "8OG5" "6O5Z" "6VRO" "7BJO" "7KVX" "7SH4" "7YB7" "8EWR" "8OGC" "6OS4" "6WFW" "7CMR" "7LG3" "7SVB" "7YBX" "8F1X" "8OMK" "6PYO" "6WMS" "7DCJ" "7LZF" "7TGQ" "7YFK" "8FDX" "8PBR" "6S7F" "6X5Q" "7E1T" "7MIC" "7U9D" "7ZC9" "8FDY" "8R79" "6SLW" "6XDB" "7F2X" "7MNU" "7UAD" "8B8Z" "8G8O" "8SKI")

# Boucle pour copier les fichiers correspondants
for id in "${pdb_ids[@]}"; do
    # Trouver tous les fichiers dans le dossier source qui commencent par l'ID
    find "$SOURCE_DIR" -name "${id}.pdb" -exec cp {} "$DEST_DIR" \;
done

echo "Les fichiers sélectionnés ont été copiés dans $DEST_DIR."
#!/bin/bash

# Définir le dossier source contenant les fichiers PDB
SOURCE_DIR="/data/home/aboussif/Projet14/deliverable/topologie/data/Ras/sapiens/pdb_filtre"

# Définir le dossier de destination pour les fichiers extraits
DEST_DIR="/data/home/aboussif/Projet14/deliverable/topologie/data/Ras/sapiens/pdb_files"

# Liste des identifiants PDB à extraire (basés sur les 4 premiers caractères)
pdb_ids=("5SGM" "6TFW" "6XI4" "7JHD" "7O08" "7ULU" "8BOK" "8G8S" "8SO1" "6GWQ" "6TWA" "6XJN" "7JO7" "7O3S" "7WCW" "8BS5" "8GM5" "8SWE" "6JVR" "6UJO" "6YUY" "7JQG" "7PRX" "7XHK" "8CIH" "8HAQ" "8UQB" "6KOJ" "6ULV" "6YYK" "7JVO" "7PWT" "7XUB" "8D6D" "8HTC" "8X72" "6KQP" "6UPR" "6ZUW" "7K2R" "7QG1" "7XVX" "8D6F" "8IIZ" "6LTK" "6VFQ" "7AXF" "7KHG" "7R3O" "7Y8D" "8DHH" "8K71" "6LXC" "6VNV" "7AZW" "7KP1" "7R5F" "7Y9C" "8E8B" "8OG5" "6O5Z" "6VRO" "7BJO" "7KVX" "7SH4" "7YB7" "8EWR" "8OGC" "6OS4" "6WFW" "7CMR" "7LG3" "7SVB" "7YBX" "8F1X" "8OMK" "6PYO" "6WMS" "7DCJ" "7LZF" "7TGQ" "7YFK" "8FDX" "8PBR" "6S7F" "6X5Q" "7E1T" "7MIC" "7U9D" "7ZC9" "8FDY" "8R79" "6SLW" "6XDB" "7F2X" "7MNU" "7UAD" "8B8Z" "8G8O" "8SKI")

# Boucle pour copier les fichiers correspondants
for id in "${pdb_ids[@]}"; do
    # Trouver tous les fichiers dans le dossier source qui commencent par l'ID
    find "$SOURCE_DIR" -name "${id}.pdb" -exec cp {} "$DEST_DIR" \;
done

echo "Les fichiers sélectionnés ont été copiés dans $DEST_DIR."
