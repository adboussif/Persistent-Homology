# SCRIPTS Documentation

## Overview
This project utilizes two scripts to process PDB files and three scripts to analyze the BCL2 protein family using Persistent Homology.

## 1. PDB File Processing Script (pdb.py)

**Description:** This script extracts alpha carbon lines from PDB files. It reads PDB files from a specified directory, extracts alpha carbon lines, and saves them in separate PDB files in an output directory.

**Key Functions:**
- `extract_alpha_carbons_lines(filename)`: Extracts alpha carbon lines from a PDB file.
- `process_subdirectory(subdir_path)`: Processes each subdirectory containing PDB files.

**Usage:**
Execute this script with the following command: `./pdb.py -d /path/to/pdb -o /path/to/output`.

## 2. Alphafold2 Processing Script (alphafold2.py)

**Description:** This script processes Alphafold2 predicted PDB files. It reads predicted PDB files, analyzes the confidence scores, and filters out low-confidence Alpha Carbons to improve the accuracy of protein structure analysis.

**Key Functions:**
- `process_alphafold_pdb(pdb_file, pkl_file, output_dir)`: Processes Alphafold2 predicted PDB files to filter Alpha Carbons based on confidence scores and saves the filtered PDB files.

**Usage:**
Execute this script with the following command: `./alphafold2.py -d /path/to/pdb_predicted -o /path/to/output`.

## 3. Protein Structure and Barcode Generation Script

**Description:** This script reads protein structures from PDB files, generates alpha complexes, computes persistence barcodes for 1D and 2D homologies, and saves the results as both PNG images and CSV files.

**Key Functions:**
- `read_coordinates_from_pdb(file_path)`: Extracts 3D coordinates of atoms from PDB files.
- `calculate_alpha_complex(coordinates)`: Uses the GUDHI library to calculate alpha complexes and generate persistence barcodes.
- `process_file(input_path, output_dir, file)`: Main function that orchestrates reading PDB files, generating barcodes, and saving results.

**Usage:**
Run automatically for each PDB file in your dataset to generate persistence barcodes and corresponding CSV files.
Execute this script with the following command: `./topologie.py -ref /path/to/pdb_ref -target path/to/pdb_target -o /path/to/output`

## 4. Wasserstein Distance Calculation and Visualization Script

**Description:** After generating persistence barcodes, this script calculates the normalized Wasserstein distance between pairs of barcodes to evaluate structural similarities. Results are visualized through heatmaps and density plots.

**Key Functions:**
- `count_alpha_carbons(file_path)`: Counts the number of alpha carbons in a PDB file to use as a normalization factor.
- `calculate_normalized_wasserstein_distance(args)`: Calculates the normalized Wasserstein distance between two sets of persistence barcodes.
- `process_pairs(csv_a_dir, pdb_a_dir, csv_b_dir, pdb_b_dir)`: Processes pairs of CSV files containing barcode data to compute distances.
- `visualize_results(distances, num_files_a, num_files_b, file_pairs, target_files, reference_files)`: Generates and saves visualizations of the distance analyses.

**Usage:**
Use this script to compare the structural similarities of proteins within the BCL2 family, based on their persistence barcodes.
Run automatically.

