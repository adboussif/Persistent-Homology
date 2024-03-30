#!/usr/bin/env python3

import argparse
import pandas as pd
import re

def clean_name(name):
    # Supprimer les préfixes "ref_" ou "target_" et les suffixes "_barcodeX.csv"
    cleaned_name = re.sub(r'^(ref_|target_)?(\d\w{3})_ca_barcode\d\.csv$', r'\2', name)
    return cleaned_name


def load_and_merge_data(distances_path, ref_annotations_path, target_annotations_path):
    # Charger les données de distances
    distances_df = pd.read_csv(distances_path)
    
    # Charger les données d'annotation cible
    target_annotations_df = pd.read_csv(target_annotations_path)
    
    # Nettoyer les noms pour correspondre
    distances_df['Target'] = distances_df['Target'].apply(clean_name)
    
    # Nettoyer les noms de référence même sans fichier d'annotations spécifique
    distances_df['Reference'] = distances_df['Reference'].apply(clean_name)
    
    # Fusionner les données de target
    merged_df = distances_df.merge(target_annotations_df.rename(columns={'Function':'Function Target'}),
                                   left_on='Target', right_on='PDB_ID', how='left')
    
    # Inclure la colonne 'Distance' dans le DataFrame final
    final_columns = ['Target', 'Function Target', 'Number of Alpha Carbons in Target', 'Distance', 'Reference']
    if ref_annotations_path:
        # Charger les données d'annotation de référence si spécifié
        ref_annotations_df = pd.read_csv(ref_annotations_path)
        merged_df = merged_df.merge(ref_annotations_df.rename(columns={'Function':'Function Reference'}),
                                    left_on='Reference', right_on='PDB_ID', how='left')
        final_columns += ['Function Reference', 'Number of Alpha Carbons in Reference']
    else:
        # Sinon, ajouter des colonnes vides pour la référence
        merged_df['Function Reference'] = ''
        merged_df['Number of Alpha Carbons in Reference'] = ''

    final_df = merged_df[final_columns]
    
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
