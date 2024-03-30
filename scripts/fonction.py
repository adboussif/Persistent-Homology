import argparse
import pandas as pd

def read_and_prepare_df(csv_path, id_column_name):
    """
    Lit un fichier CSV et prépare le DataFrame en renommant la colonne d'identifiant.
    """
    df = pd.read_csv(csv_path)
    df.rename(columns={'PDB_ID': id_column_name}, inplace=True)
    return df

def merge_dataframes(distance_path, ref_path, target_path, output_path):
    """
    Fusionne les DataFrames des distances, références, et targets dans un seul DataFrame.
    """
    # Lire et préparer les DataFrames
    df_distances = pd.read_csv(distance_path)
    df_ref = read_and_prepare_df(ref_path, 'Reference')
    df_target = read_and_prepare_df(target_path, 'Target')

    # Fusionner les informations de référence et de target avec les distances
    merged_df = pd.merge(df_distances, df_ref, on='Reference', how='left')
    final_df = pd.merge(merged_df, df_target, on='Target', how='left')

    # Sauvegarder le DataFrame final
    final_df.to_csv(output_path, index=False)
    print(f"Results saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine distance, reference, and target information into a single DataFrame.")
    parser.add_argument('-d', '--distance', required=True, help="Path to the CSV file containing distance information.")
    parser.add_argument('-ref', '--reference', required=True, help="Path to the CSV file containing reference information.")
    parser.add_argument('-t', '--target', required=True, help="Path to the CSV file containing target information.")
    parser.add_argument('-o', '--output', required=True, help="Path to save the combined CSV file.")

    args = parser.parse_args()

    merge_dataframes(args.distance, args.reference, args.target, args.output)
