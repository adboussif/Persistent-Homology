# Dataset for Persistent Homology Analysis on BCL2 Protein Family

## Overview

This document provides details on the datasets used for the analysis of the BCL2 protein family through persistent homology. The datasets include 111 sequences from a Reference Proteome of validated BCL2 proteins and a Control Proteome from well-characterized species (already Alpha Carbones filtered with `pdb.py`)

## Datasets Description

### Reference Proteome (`bcl2_111_seq.fst`)
- **Description:** This dataset consists of 111 sequences of BCL2 proteins that have been validated and curated with the expertise of collaborator Nikolay Popgeorgiev.
- **Purpose:** To serve as a solid reference for our analysis, enabling the comparison and validation of potential BCL2 proteins identified in our study.

### Control Proteome (Homo sapiens, Drosophila melanogaster, Caenorhabditis elegans, Danio rerio)
- **Description:** Comprises sequences from well-characterized proteomes of species like *Homo sapiens*, *Danio rerio*, *Drosophila melanogaster*, and *Caenorhabditis elegans*. The sequences are filtered based on their size (150 to 600 amino acids) from the PDB database.
- **Purpose:** To refine and validate the approach by filtering out less probable candidates for BCL2 proteins and managing data volume efficiently.

### PDB files, Barcodes and Plots
- **Description:** Results from the workflow for each Control Proteome against Reference Proteome.

For more information on how these datasets are utilized in our analysis and how we obtain the Results, please refer to the [Project Overview](#project-overview) and [USAGE](#usage)section.
