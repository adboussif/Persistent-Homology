#!/usr/bin/env python3

import os
from functools import partial
from multiprocessing import Pool
from Bio.PDB import PDBParser
import gudhi as gudhi
import matplotlib.pyplot as plt
import pandas as pd

def read_coordinates_from_pdb(file_path):
    parser = PDBParser()
    structure = parser.get_structure("protein", file_path)
    coordinates = []
    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    coordinates.append(atom.get_coord())
    return coordinates

def calculate_rips_complex(coordinates):
    rips_complex = gudhi.RipsComplex(points=coordinates)
    simplex_tree = rips_complex.create_simplex_tree(max_dimension=1)
    barcodes = simplex_tree.persistence()
    return barcodes

def process_file(input_path, output_dir, file):
    pdb_file_path = os.path.join(input_path, file)
    coordinates = read_coordinates_from_pdb(pdb_file_path)
    barcodes = calculate_rips_complex(coordinates)
    barcode_df = pd.DataFrame(barcodes, columns=["Birth", "Death"])
    barcode_file_path = os.path.join(output_dir, f"{file[:-4]}_barcodes.csv")
    barcode_df.to_csv(barcode_file_path, index=False)
    plt.figure(figsize=(8, 6))
    gudhi.plot_persistence_barcode(barcodes)
    plt.title(f"Barcodes for file {file[:-4]}")
    plt.xlabel("Birth")
    plt.ylabel("Death")
    plt.savefig(os.path.join(output_dir, f"{file[:-4]}_barcode.png"))
    plt.close()

if __name__ == "__main__":
    input_path = "/data/home/tfoussenisalamicisse/projet_hp/all_prot_structure_coord"
    output_dir = "/data/home/tfoussenisalamicisse/projet_hp/res_dim_1"


     # Vérifier si le dossier de sortie existe, sinon le créer
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    files = os.listdir(input_path)
    process_file_partial = partial(process_file, input_path, output_dir)

    with Pool() as pool:
        pool.starmap(process_file_partial, [(file,) for file in files if file.endswith('.pdb')])
