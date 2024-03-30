#!/usr/bin/env python3

#!/usr/bin/env python3

import os
import pandas as pd
from Bio.PDB import PDBParser
import gudhi as gd
import numpy as np

def read_coordinates_from_pdb(file_path):
    parser = PDBParser()
    structure = parser.get_structure("protein", file_path)
    coordinates = []
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    coordinates.append(atom.get_coord())
    return np.array(coordinates)

def calculate_rips_complex(file_path):
    coordinates = read_coordinates_from_pdb(file_path)
    rips_complex = gd.RipsComplex(points=coordinates)
    simplex_tree = rips_complex.create_simplex_tree(max_dimension=3)
    return simplex_tree.persistence()

if __name__ == "__main__":
    pdb_directory = "/data/home/tfoussenisalamicisse/projet_hp/pdb_files_zebrafish/pdb_files/pdb_filtre/pdb_filtre/pdb_ca_files"
    output_directory = "/data/home/tfoussenisalamicisse/projet_hp/pdb_files_zebrafish/png_csv_results"

    os.makedirs(output_directory, exist_ok=True)

    for filename in os.listdir(pdb_directory):
        if filename.endswith(".pdb"):
            file_path = os.path.join(pdb_directory, filename)
            barcodes = calculate_rips_complex(file_path)
            barcode_df = pd.DataFrame(barcodes, columns=["Birth", "Death"])
            output_file_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}_barcodes.csv")
            barcode_df.to_csv(output_file_path, index=False)


