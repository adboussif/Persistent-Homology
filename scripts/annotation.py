#!/usr/bin/env python3

import os
import argparse
import requests
import pandas as pd
import time

def submit_id_mapping_request(from_db, to_db, ids):
    url = 'https://rest.uniprot.org/idmapping/run'
    # Convertir la liste d'IDs en une chaîne de caractères séparée par des virgules
    ids_str = ','.join(ids)
    # Les données sont envoyées comme un formulaire
    data = {
        'from': from_db,
        'to': to_db,
        'ids': ids_str
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json()['jobId']
    else:
        raise Exception(f"Error submitting ID mapping request: {response.status_code} {response.text}")



def check_id_mapping_results(job_id):
    results_url = f'https://rest.uniprot.org/idmapping/results/{job_id}'
    while True:
        response = requests.get(results_url)
        if response.status_code == 200:
            return response.json()  # This should be the final results in JSON format
        elif response.status_code == 202:
            print("Results not ready yet, waiting...")
            time.sleep(30)  # Wait for 5 seconds before checking again
        else:
            raise Exception(f"Error fetching ID mapping results: {response.status_code} {response.text}")

def get_pdb_ids(pdb_dir):
    pdb_ids = []
    for filename in os.listdir(pdb_dir):
        if filename.endswith(".pdb"):
            pdb_id = filename[:-4]  # Removing the .pdb extension to get the PDB ID
            pdb_ids.append(pdb_id)
    return pdb_ids

def get_uniprot_ids_from_pdb(pdb_ids):
    job_id = submit_id_mapping_request('PDB', 'UniProtKB', pdb_ids)
    print(f"Job submitted successfully. Job ID: {job_id}")
    uniprot_results_json = check_id_mapping_results(job_id)
    uniprot_mapping = process_mapping_results(uniprot_results_json)
    return uniprot_mapping

def process_mapping_results(json_data):
    mapping_results = {}
    for result in json_data.get('results', []):
        pdb_id = result.get('from')
        uniprot_id = result.get('to')
        mapping_results[pdb_id] = uniprot_id
    return mapping_results

def get_go_terms_from_uniprot(uniprot_id):
    url = f'https://rest.uniprot.org/uniprotkb/{uniprot_id}/function'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        go_terms = [go.get('id') for go in data.get('goTerms', []) if go.get('aspect') == 'B']  # Aspect 'F' for molecular function
        return go_terms
    return []

def main(pdb_dir):
    output_csv_path = os.path.join(pdb_dir, "results_annotation.csv")
    pdb_ids = get_pdb_ids(pdb_dir)
    print(f"Found PDB IDs: {pdb_ids}")

    # Fetch the UniProt IDs corresponding to the PDB IDs
    uniprot_mapping = get_uniprot_ids_from_pdb(pdb_ids)
    
    # Build a DataFrame with PDB IDs, UniProt IDs, and GO Terms
    results_data = []
    for pdb_id, uniprot_id in uniprot_mapping.items():
        go_terms = get_go_terms_from_uniprot(uniprot_id)
        results_data.append([pdb_id, uniprot_id, "; ".join(go_terms)])
    
    results_df = pd.DataFrame(results_data, columns=['PDB_ID', 'UniProt_ID', 'GO_Terms'])
    results_df.to_csv(output_csv_path, index=False)
    print(f"Results saved to {output_csv_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script pour récupérer les IDs UniProt à partir des IDs PDB et annoter les protéines.")
    parser.add_argument('-p', '--pdb', required=True, help="Chemin vers le dossier contenant les fichiers PDB.")
    args = parser.parse_args()
    main(args.pdb)
