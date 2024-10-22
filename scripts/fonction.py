#!/usr/bin/env python3

import argparse
import pandas as pd
import re

def clean_name(name):
    # Retirer les préfixes 'target_' ou 'ref_' et les suffixes '_ca' ou '_barcode'
    return re.sub(r'^(target_|ref_)?(.*?)(_ca|_barcode)?$', r'\2', name)

def load_and_merge_data(distances_path, ref_annotations_path, target_annotations_path):
    # Charger les données de distances
    distances_df = pd.read_csv(distances_path)
    
    # Nettoyer les noms dans les colonnes 'Target' et 'Reference'
    distances_df['Target'] = distances_df['Target'].apply(clean_name)
    
    # Charger les données d'annotation cible et nettoyer
    target_annotations_df = pd.read_csv(target_annotations_path)
    target_annotations_df['PDB_ID'] = target_annotations_df['PDB_ID'].apply(clean_name)
    
    # Fusionner les données de target
    merged_df = distances_df.merge(target_annotations_df[['PDB_ID', 'Function']],
                                   left_on='Target', right_on='PDB_ID', how='left')
    merged_df.rename(columns={'Function': 'Function Target'}, inplace=True)
    
    # Ajouter des colonnes de 'Reference' à partir des distances_df si -ref n'est pas fourni
    if not ref_annotations_path:
        merged_df['Function Reference'] = None  # Créer une colonne vide pour 'Function Reference'
        merged_df['Number of Alpha Carbons in Reference'] = None  # Créer une colonne vide pour 'Number of Alpha Carbons in Reference'
    
    # Charger et fusionner les données de référence si fournies
    if ref_annotations_path:
        ref_annotations_df = pd.read_csv(ref_annotations_path)
        ref_annotations_df['PDB_ID'] = ref_annotations_df['PDB_ID'].apply(clean_name)
        merged_df = merged_df.merge(ref_annotations_df[['PDB_ID', 'Function']],
                                    left_on='Reference', right_on='PDB_ID', how='left')
        merged_df.rename(columns={'Function': 'Function Reference'}, inplace=True)

    # Inclure la colonne 'Distance' dans le DataFrame final
    final_df = merged_df[['Target', 'Function Target', 'Number of Alpha Carbons in Target',
                          'Distance', 'Reference', 'Function Reference', 'Number of Alpha Carbons in Reference']].fillna("N/A")

    return final_df

def save_to_csv(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"CSV réarrangé sauvegardé à {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Réarranger et fusionner les données de distance et d'annotation.")
    parser.add_argument('-d', '--distance', required=True, help="Chemin vers le fichier CSV des distances.")
    parser.add_argument('-ref', '--reference', help="Chemin facultatif vers le fichier CSV d'annotations de référence.")
    parser.add_argument('-target', '--target', required=True, help="Chemin vers le fichier CSV d'annotations cibles.")
    parser.add_argument('-o', '--output', required=True, help="Chemin vers le fichier CSV de sortie réarrangé.")
    
    args = parser.parse_args()
    
    final_df = load_and_merge_data(args.distance, args.reference, args.target)
    save_to_csv(final_df, args.output)

if __name__ == "__main__":
    main()
