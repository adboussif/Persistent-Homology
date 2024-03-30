#!/usr/bin/env python3

import argparse
import pandas as pd

def load_and_merge_data(distances_path, ref_annotations_path, target_annotations_path):
    # Charger les données de distances
    distances_df = pd.read_csv(distances_path)
    
    # Charger les données d'annotation
    ref_annotations_df = pd.read_csv(ref_annotations_path)
    target_annotations_df = pd.read_csv(target_annotations_path)
    
    # Nettoyer les colonnes pour correspondre aux ID PDB
    distances_df['Reference'] = distances_df['Reference'].str.extract(r'(\d\w{3})')  # Extrait les ID PDB de Reference
    distances_df['Target'] = distances_df['Target'].str.extract(r'(\d\w{3})')  # Extrait les ID PDB de Target
    
    # Fusionner les données en s'assurant que les colonnes correspondent
    merged_df = distances_df.merge(target_annotations_df.rename(columns={'Function':'Function Target'}),
                                   left_on='Target', right_on='PDB_ID', how='left')
    merged_df = merged_df.merge(ref_annotations_df.rename(columns={'Function':'Function Reference'}),
                                left_on='Reference', right_on='PDB_ID', how='left')
    
    # Inclure la colonne 'Distance' dans le DataFrame final
    final_df = merged_df[['Target', 'Function Target', 'Number of Alpha Carbons in Target',
                          'Reference', 'Function Reference', 'Number of Alpha Carbons in Reference', 'Distance']]
    
    return final_df

def save_to_csv(df, output_path):
    df.to_csv(output_path, index=False)
    print(f"CSV réarrangé sauvegardé à {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Réarranger et fusionner les données de distance et d'annotation.")
    parser.add_argument('-d', '--distance', required=True, help="Chemin vers le fichier CSV des distances.")
    parser.add_argument('-ref', '--reference', required=True, help="Chemin vers le fichier CSV d'annotations de référence.")
    parser.add_argument('-target', '--target', required=True, help="Chemin vers le fichier CSV d'annotations cibles.")
    parser.add_argument('-o', '--output', required=True, help="Chemin vers le fichier CSV de sortie réarrangé.")
    
    args = parser.parse_args()
    
    final_df = load_and_merge_data(args.distance, args.reference, args.target)
    save_to_csv(final_df, args.output)

if __name__ == "__main__":
    main()
