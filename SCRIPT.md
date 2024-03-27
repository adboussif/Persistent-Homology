# SCRIPTS Documentation

## Overview
This project utilizes two scripts to analyze the BCL2 protein family using Persistent Homology.

## 1. Protein Structure and Barcode Generation Script

**Description:** This script reads protein structures from PDB files, generates alpha complexes, computes persistence barcodes for 1D and 2D homologies, and saves the results as both PNG images and CSV files.

**Key Functions:**
- `read_coordinates_from_pdb(file_path)`: Extracts 3D coordinates of atoms from PDB files.
- `calculate_alpha_complex(coordinates)`: Uses the GUDHI library to calculate alpha complexes and generate persistence barcodes.
- `process_file(input_path, output_dir, file)`: Main function that orchestrates reading PDB files, generating barcodes, and saving results.

**Usage:**
Run the script for each PDB file in your dataset to generate persistence barcodes and corresponding CSV files.

## 2. Wasserstein Distance Calculation and Visualization Script

**Description:** After generating persistence barcodes, this script calculates the normalized Wasserstein distance between pairs of barcodes to evaluate structural similarities. Results are visualized through heatmaps and density plots.

**Key Functions:**
- `count_alpha_carbons(file_path)`: Counts the number of alpha carbons in a PDB file to use as a normalization factor.
- `calculate_normalized_wasserstein_distance(args)`: Calculates the normalized Wasserstein distance between two sets of persistence barcodes.
- `process_pairs(csv_a_dir, pdb_a_dir, csv_b_dir, pdb_b_dir)`: Processes pairs of CSV files containing barcode data to compute distances.
- `visualize_results(distances, num_files_a, num_files_b, file_pairs, target_files, reference_files)`: Generates and saves visualizations of the distance analyses.

**Usage:**
Use this script to compare the structural similarities of proteins within the BCL2 family, based on their persistence barcodes.

**Implementation Note:**
Ensure to adjust the directory paths and file names according to your project structure when using these scripts.
