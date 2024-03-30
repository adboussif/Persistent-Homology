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

def check_job_status(job_id):
    status_url = f'https://rest.uniprot.org/idmapping/status/{job_id}'
    while True:
        response = requests.get(status_url)
        if response.status_code == 200:
            status = response.json()
            if status.get('jobStatus') == 'FINISHED':
                return True
            elif status.get('jobStatus') == 'RUNNING':
                print("Job is still running. Waiting before checking again...")
                time.sleep(300)
            else:
                return False
        else:
            raise Exception(f"Error fetching job status: {response.status_code} {response.text}")
    return False

def get_uniprot_ids_from_pdb(pdb_ids):
    job_id = submit_id_mapping_request('PDB', 'UniProtKB', pdb_ids)
    print(f"Job submitted successfully. Job ID: {job_id}")
    if check_job_status(job_id):
        results_url = f'https://rest.uniprot.org/idmapping/results/{job_id}'
        response = requests.get(results_url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error fetching ID mapping results: {response.status_code} {response.text}")
    else:
        raise Exception("Job did not finish successfully.")

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
        uniprot_id = result.get('to', {}).get('id', '')
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
            go_terms = [go.get('id') for go in data.get('goTerms', []) if go.get('aspect') == 'B']  # Assuming 'B' for biological process
            return "; ".join(go_terms)
    return ""

def main(pdb_dir):
    output_csv_path = os.path.join(pdb_dir, "results_annotation.csv")
    pdb_ids = get_pdb_ids(pdb_dir)
    print(f"Found PDB IDs: {pdb_ids}")

    try:
        uniprot_results_json = get_uniprot_ids_from_pdb(pdb_ids)
        uniprot_mapping = process_mapping_results(uniprot_results_json)
    except Exception as e:
        print(f"An error occurred while mapping PDB to UniProt IDs: {e}")
        uniprot_mapping = {}

    results_data = []
    for pdb_id in pdb_ids:
        uniprot_id = uniprot_mapping.get(pdb_id, "")
        go_terms = get_go_terms_from_uniprot(uniprot_id) if uniprot_id else get_function_from_pdb_file(os.path.join(pdb_dir, pdb_id + '.pdb'))
        results_data.append([pdb_id, uniprot_id, go_terms])

    results_df = pd.DataFrame(results_data, columns=['PDB_ID', 'UniProt_ID', 'Function/GO_Terms'])
    results_df.to_csv(output_csv_path, index=False)
    print(f"Results saved to {output_csv_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to fetch UniProt IDs from PDB IDs and annotate proteins.")
    parser.add_argument('-p', '--pdb', required=True, help="Path to the directory containing PDB files.")
    args = parser.parse_args()
    main(args.pdb)
