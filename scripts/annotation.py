#!/usr/bin/env python3

import os
import argparse
import requests
import pandas as pd
import time

def submit_id_mapping_request(from_db, to_db, ids):
    url = 'https://rest.uniprot.org/idmapping/run'
    ids_str = ','.join(ids)
    data = {'from': from_db, 'to': to_db, 'ids': ids_str}
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
            return response.json()
        elif response.status_code == 202:
            print("Results not ready yet, waiting...")
            time.sleep(30)
        else:
            raise Exception(f"Error fetching ID mapping results: {response.status_code} {response.text}")

def get_pdb_ids(pdb_dir):
    pdb_ids = []
    for filename in os.listdir(pdb_dir):
        if filename.endswith(".pdb"):
            pdb_id = filename[:-4]
            pdb_ids.append(pdb_id)
    return pdb_ids

def process_mapping_results(json_data):
    mapping_results = {}
    for result in json_data.get('results', []):
        pdb_id = result.get('from')
        uniprot_id = result.get('to')
        mapping_results[pdb_id] = uniprot_id
    return mapping_results

def get_function_from_pdb_file(pdb_file_path):
    with open(pdb_file_path, 'r') as file:
        for line in file:
            if line.startswith("HEADER"):
                description = line[10:50].strip()
                return description
    return "Function not found"

def get_go_terms_from_uniprot(uniprot_id):
    if uniprot_id:
        url = f'https://rest.uniprot.org/uniprotkb/{uniprot_id}/function'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            go_terms = [go.get('id') for go in data.get('goTerms', []) if go.get('aspect') == 'B']
            return "; ".join(go_terms)
    return ""

def main(pdb_dir):
    output_csv_path = os.path.join(pdb_dir, "results_annotation.csv")
    pdb_ids = get_pdb_ids(pdb_dir)
    uniprot_mapping = get_uniprot_ids_from_pdb(pdb_ids)

    results_data = []
    for pdb_id in pdb_ids:
        uniprot_id = uniprot_mapping.get(pdb_id, "")
        go_terms = get_go_terms_from_uniprot(uniprot_id)
        if not go_terms:
            pdb_file_path = os.path.join(pdb_dir, pdb_id + '.pdb')
            go_terms = get_function_from_pdb_file(pdb_file_path)
        results_data.append([pdb_id, uniprot_id, go_terms])

    results_df = pd.DataFrame(results_data, columns=['PDB_ID', 'UniProt_ID', 'Function/GO_Terms'])
    results_df.to_csv(output_csv_path, index=False)
    print(f"Results saved to {output_csv_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to fetch UniProt IDs from PDB IDs and annotate proteins.")
    parser.add_argument('-p', '--pdb', required=True, help="Path to the directory containing PDB files.")
    args = parser.parse_args()
    main(args.pdb)
