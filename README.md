# Persistent Homology Analysis on BCL2 Protein Family

This repository houses the Python scripts and analysis for the study of the BCL2 protein family using Persistent Homology.

## Project Context

Apoptosis, or programmed cell death, is regulated by the Bcl-2 family of proteins, which can promote or inhibit the process. Our project leverages bioinformatics and topological data analysis (TDA) to enhance the identification and classification of protein families, particularly focusing on the BCL2 family. The detailed project context and problematic can be found in the `PROJECT_CONTEXT.md` file.

## Overview

The project workflow includes evaluating 3D structures of BCL2 proteins, analyzing them using TDA, and comparing structures with Wasserstein distances. The `GUDHI Python library` is utilized to understand the persistent homology of BCL2 proteins, generating barcodes and Wasserstein distance matrices for analysis.

## Dataset

The dataset consists of validated BCL2 protein sequences and putative BCL2 sequences across various animal proteomes. Details about the datasets are available in the `DATASET.md` file.

## Objectives

1. **Structure Evaluation**: Use AlphaFold2 for predicting and evaluating 3D structures of BCL2 proteins. We focus on high-confidence structures (pLDDT > 70%) for reliable analysis.
   
2. **Topological Data Analysis**: Implement TDA to study the persistent homology of BCL2 proteins, generating barcodes and a Wasserstein distance matrix for identifying significant structural similarities.

3. **Control Proteome Analysis**: Extend the analysis to a control proteome, refining the approach and validating the method's effectiveness in distinguishing BCL2 proteins and potential false positives/negatives.

## Pipeline

A Python pipeline processes primary protein sequences through AlphaFold2 for structural predictions, followed by an analysis of persistent homology. The pipeline is designed to:

- Predict and evaluate 3D structures of BCL2 proteins.
- Select high-confidence structures based on Ca pLDDT values.
- Generate barcodes and Wasserstein distances using the GUDHI Python library.

## Usage

Instructions for running the analysis are detailed in `USAGE.md`.

## Documentation

Scripts used throughout the project are well-documented. Please refer to `SCRIPTS.md` for more information.

## Troubleshooting

For common issues encountered during the project setup or execution, please check `TROUBLESHOOTING.md`.

## Contributing

Contributions to the project are welcome. For contributing guidelines, please read `CONTRIBUTING.md`.

## License

This project is licensed under the [MIT License](LICENSE).
