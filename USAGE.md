# Using the Scripts for Persistent Homology Analysis

This project includes three main scripts designed to filter Alpha Carbones in PDB file (from database or predicted by Alphafold2) and to analyze protein structures through persistence barcodes and calculate Wasserstein distances for comparison.

## Requirements

- Python 3.x
- Libraries: GUDHI, BioPython, matplotlib, seaborn, pandas, numpy, pickle, functools, argparse, csv
- PDB files of protein structures

````markdown
```bash
pip install GUDHI biopython matplotlib seaborn pandas numpy pickle functools argparse csv



## Step 1: Preparing PDB files / Predicting with Alphafold2

### Process

1. **Predicting with ALphafold2 :** We used NMRbox, a VM which allows us to perform Alphafold2 prediction from our set of 111 primary BCL2 sequences.
2bis. **Processing Alpha Carbonne Capture(Alphafold2)** Use alphafold.py which will process pdb file predicted by Alphafold and keep well predicted atomes based on their pLDDT.
2bis. **Processing Alpha Carbonne Capture(PDBdatabase)** Use pdb.py which will process pdb file downloaded on the PDB databse, and remove all atomes except alpha carbones.
3. **Run the script:** Execute the script that suits your dataset.

### Output

- PDB files containing only alpha carbones coordinates.
- CSV file containing resume of before and after PDB files based on the pLDDT and number of alpha carbone before and after select_ca.py

## Step 2: Generating Persistence Barcodes

#### Process

1. **Prepare Your PDB Files:** Place your protein structure files (in PDB format, with only alpha carbon atoms) in the appropriate input directory. The input directories are specified when running the `topologie.py` script with the `-ref` and `-target` options for the reference and target protein structures, respectively.

2. **Run the Script:** Execute the `topologie.py` script, specifying the reference (`-ref`) and target (`-target`) directories, and the output directory (`-o`) where you want the results to be saved.
Example usage:
````markdown
```bash
./topologie.py -ref path/to/reference -target path/to/target -o path/to/output

#### Output

- Persistence barcodes as PNG images, stored in the specified output directory under `reference/barcodes` and `target/barcodes`.
- CSV files containing barcode data, located in `reference/output` and `target/output`.

### Step 3: Calculating Wasserstein Distance and Visualization

The `topologie.py` script also handles the calculation of Wasserstein distances between persistence barcodes and their visualization. The steps described in Step 2 are sufficient for the entire process from barcode generation to distance calculation and visualization.

#### Results

- Heatmap images visualizing the Wasserstein distances between protein structures from the reference and target sets. These images are saved in the specified output directory.
- A CSV file `distance_results.csv` listing the calculated distances for further analysis. This file is also saved in the specified output directory.

This streamlined process simplifies the analysis of protein structures using topological data analysis methods, from persistence barcode generation to comparing structures with Wasserstein distances.

## Additional Information

Ensure all prerequisites are installed before running the scripts to avoid any execution errors.
