# Using the Scripts for Persistent Homology Analysis

This project includes two main scripts designed to analyze persistent homology in proteins, focusing on the BCL2 protein family. Here's how to use them.

## Requirements

- Python 3.x
- Libraries: GUDHI, BioPython, matplotlib, seaborn, pandas, numpy, pickle
- PDB files of protein structures

## Step 1: Preparing PDB files / Predicting with Alphafold2

### Process

1. **Predicting with ALphafold2 :** We used NMRbox, a VM which allows us to perform Alphafold2 prediction from our set of 111 primary BCL2 sequences.
2bis. **Processing Alpha Carbonne Capture(Alphafold2)** Use select_ca.py which will process pdb file predicted by Alphafold and keep well predicted atomes based on their pLDDT.
2bis. **Processing Alpha Carbonne Capture(PDBdatabase)** Use select_CA.py which will process pdb file downloaded on the PDB databse, and remove all atomes except alpha carbones.
3. **Run the script:** Execute the script that suits your dataset.

### Output

- PDB files containing only alpha carbones coordinates.
- CSV file containing resume of before and after PDB files based on the pLDDT and number of alpha carbone before and after select_ca.py

## Step 2: Generating Persistence Barcodes

### Process

1. **Prepare your PDB files:** Ensure your protein structure files (in PDB format with only alpha carbones atomes) are placed in the appropriate input directory.
2. **Configure the script:** Set the `input_path` to your directory of PDB files and `output_dir` to where you want the barcode images and CSV files saved.
3. **Run the script:** Execute `alpha.py` to analyze the PDB files and generate persistence barcodes.

### Output

- Persistence barcodes as PNG images.
- CSV files containing barcode data.

## Step 2: Calculating Wasserstein Distance and Visualization

### Setup

1. **Check for persistence barcodes:** Ensure Step 2 has been completed and barcode data is available.
2. **Configure paths in the script:** Set `csv_a_dir`, `pdb_a_dir`, `csv_b_dir`, and `pdb_b_dir` to the directories containing your CSV and PDB files, respectively.
3. **Execute the script:** Run `analyse.py` to compute Wasserstein distances and visualize the results.

### Results

- A heatmap visualizing the Wasserstein distances between protein structures.
- A CSV file listing the calculated distances for further analysis.

## Additional Information

Refer to the individual scripts for more detailed documentation on parameters and additional functionalities. Ensure all prerequisites are installed before running the scripts to avoid any execution errors.
