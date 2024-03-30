#!/usr/bin/env python3

import argparse
import pandas as pd
from scipy.stats import ks_2samp, mannwhitneyu
from statsmodels.stats.multitest import multipletests
import os

def perform_ks_test(ref_distances, target_distances):
    ks_statistic, ks_p_value = ks_2samp(ref_distances, target_distances)
    return ks_statistic, ks_p_value

def calculate_p_values(distances_df, comparison_distances):
    p_values = []
    for distance in distances_df['Distance']:
        stat, p = mannwhitneyu([distance], comparison_distances, alternative='two-sided')
        p_values.append(p)
    return p_values

def adjust_p_values(p_values):
    rejected, p_values_corrected, _, _ = multipletests(p_values, alpha=0.05, method='fdr_bh')
    return p_values_corrected

def load_and_prepare_data(ref_path, target_path):
    ref_df = pd.read_csv(ref_path)
    target_df = pd.read_csv(target_path)
    return ref_df['Distance'].values, target_df['Distance'].values

def main():
    parser = argparse.ArgumentParser(description="Perform statistical tests and save results.")
    parser.add_argument('-ref', '--ref', required=True, help="Path to the reference CSV file.")
    parser.add_argument('-target', '--target', required=True, help="Path to the target CSV file.")
    parser.add_argument('-o', '--output', required=True, help="Output directory for the enriched CSV file.")

    args = parser.parse_args()
    
    # Load and prepare data
    ref_distances, target_distances = load_and_prepare_data(args.ref, args.target)
    
    # Perform Kolmogorov-Smirnov test
    ks_statistic, ks_p_value = perform_ks_test(ref_distances, target_distances)
    print(f"KS Statistic: {ks_statistic}")
    print(f"KS P-value: {ks_p_value}")

    # Calculate p-values for each distance in target compared to reference
    target_df = pd.read_csv(args.target)
    p_values = calculate_p_values(target_df, ref_distances)
    target_df['P-Value'] = p_values

    # Adjust p-values with FDR
    p_values_corrected = adjust_p_values(p_values)
    target_df['Q-Value'] = p_values_corrected

    # Save to CSV
    output_file_path = os.path.join(args.output, 'enriched_target_df.csv')
    target_df.to_csv(output_file_path, index=False)
    print(f"Enriched CSV file saved to {output_file_path}")

if __name__ == "__main__":
    main()
