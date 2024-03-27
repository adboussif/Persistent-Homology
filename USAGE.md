# Using the Scripts for Persistent Homology Analysis

This project includes two main scripts designed to filter Alpha Carbons in PDB files (from database or predicted by Alphafold2), a workflow of three scripts to analyze protein structures through persistence barcodes and calculate Wasserstein distances for comparison with Alpha Conplex construction and two scripts to perform the same analysis but with Rips Complex construction.

## Requirements

- Python 3.x
- Libraries: GUDHI, BioPython, matplotlib, seaborn, pandas, numpy, pickle, functools, argparse, csv
- PDB files of protein structures

```bash
pip install GUDHI biopython matplotlib seaborn pandas numpy pickle functools argparse csv
```

## Step 1: Preparing PDB files / Predicting with Alphafold2

### Process

1. **Predicting with Alphafold2:** We used NMRbox, a VM which allows us to perform Alphafold2 prediction from our set of 111 primary BCL2 sequences.
2. **Processing Alpha Carbon Capture (Alphafold2):** Use `alphafold.py` which will process pdb file predicted by Alphafold and keep well predicted atoms based on their pLDDT.
3. **Processing Alpha Carbon Capture (PDB database):** Use `pdb.py` which will process pdb file downloaded from the PDB database and remove all atoms except alpha carbones.
4. **Run the script:** Execute the script that suits your dataset.

Example usage:

```bash
./alphafold.py -d /path/to/pdb_predicted -o /path/to/output
./pdb.py -d /path/to/pdb -o /path/to/output
```

### Output

- PDB files containing only alpha carbon coordinates.
- CSV file containing a summary of `alphafold.py`

## Step 2a: Generating Persistence Barcodes (AlphaComplex)

#### Process

1. **Prepare Your PDB Files:** Place your protein structure files (in PDB format, with only alpha carbon atoms) in the appropriate input directory. The input directories are specified when running the `topologie.py` script with the `-ref` and `-target` options for the reference and target protein structures, respectively.
2. **Run the Script:** Execute the `topologie.py` script, specifying the reference (`-ref`) and target (`-target`) directories, and the output directory (`-o`) where you want the results to be saved.

Example usage:

```bash
./topologie.py -ref path/to/reference -target path/to/target -o path/to/output
```

#### Output

- Persistence barcodes as PNG images, stored in the specified output directory under `reference/barcodes` and `target/barcodes`.
- CSV files containing barcode data, located in `reference/output` and `target/output`.

## Step 3a: Calculating Wasserstein Distance and Visualization (AlphaComplex)

The `topologie.py` script also handles the calculation of Wasserstein distances between persistence barcodes on the same dimension and their visualization. The steps described in Step 2 are sufficient for the entire process from barcode generation to distance calculation and visualization.

#### Results

- A PNG file `visualization.png`(Heatmap and Density plot) visualizing the Wasserstein distances between protein structures from the reference and target sets. These images are saved in the specified output directory.
- A CSV file `distance_results.csv` listing the calculated distances for further analysis. This file is also saved in the specified output directory.

This streamlined process simplifies the analysis of protein structures using topological data analysis methods, from persistence barcode generation to comparing structures with Wasserstein distances.

## Step 2b: Calculating Wasserstein Distance and Visualization (RipsComplex)

**Prepare Your PDB Files:** Place your protein structure files (in PDB format, with only alpha carbon atoms) in the appropriate input directory. The input and output directories have to be specified in the `rips_complex.py` script itself.

#### Results

- Persistence barcodes as PNG images, stored in the specified output directory.
- CSV files containing barcode data, also stored in the specified output directory.

## Step 3b: Calculating Wasserstein Distance and Visualization (RipsComplex)

1. **Prepare Your PDB Files:** Place your protein structure files (in PDB format, with only alpha carbon atoms) in the appropriate input directory. The input directories are have to be specified in the `analyse.py` script.
2. **Prepare Your CSV Files:** Place your barcode files (in CSV format) in the appropriate input directory. Also the input and output directories have to be specified in the `analyse.py`.

#### Results

- A PNG file `visualization.png`(Heatmap and Density plot) visualizing the Wasserstein distances between protein structures from the reference and target sets. These images are saved in the specified output directory.
- A CSV file `distance_results.csv` listing the calculated distances for further analysis. This file is also saved in the specified output directory.

This streamlined process simplifies the analysis of protein structures using topological data analysis methods, from persistence barcode generation to comparing structures with Wasserstein distances.

## Additional Information

Ensure all prerequisites are installed before running the scripts to avoid any execution errors.
