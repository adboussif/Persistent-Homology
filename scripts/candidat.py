#!/usr/bin/env python3

import argparse
import pandas as pd

def filtrer_candidats(fichier_donnees, ajouter_infos_reference, fichier_sortie):
    df = pd.read_csv(fichier_donnees)
    
    # Filtrer les données basées sur p-value et q-value inférieures ou égales à 0.05
    df_filtre = df[(df['pvalue'] <= 0.05) & (df['qvalue'] <= 0.05)]

    # Sélectionner les colonnes d'intérêt
    colonnes = ['target', 'fonction_target', 'reference', 'pvalue', 'qvalue']
    if ajouter_infos_reference:
        colonnes += ['infos_reference']  # Ajoutez le nom correct de votre colonne d'informations de référence
    df_final = df_filtre[colonnes]

    # Ajouter une colonne 'rang' basée sur le rang des p-values
    df_final['rang'] = df_final['pvalue'].rank(method='min')

    # Sauvegarder le résultat dans un nouveau fichier CSV
    df_final.to_csv(fichier_sortie, index=False)
    print(f"Les résultats filtrés ont été sauvegardés dans {fichier_sortie}")

def main():
    parser = argparse.ArgumentParser(description="Filtrer les paires de protéines candidates basées sur les p-values et q-values.")
    parser.add_argument('-d', '--data', required=True, help="Chemin vers le fichier CSV des données.")
    parser.add_argument('-a', '--add_ref_info', action='store_true', help="Inclure les informations de référence supplémentaires.")
    parser.add_argument('-o', '--output', required=True, help="Dossier de sortie pour le fichier CSV filtré.")
    
    args = parser.parse_args()

    # Construire le chemin de sortie pour le fichier CSV
    fichier_sortie = f"{args.output}/resultats_filtres.csv"

    filtrer_candidats(args.data, args.add_ref_info, fichier_sortie)

if __name__ == "__main__":
    main()
