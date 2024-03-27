# Project Context for Persistent Homology Analysis on BCL2 Protein Family

## Understanding Apoptosis and the BCL2 Family

Apoptosis, a critical physiological process, selectively eliminates cells to maintain health and prevent disease. The BCL2 family of proteins plays a pivotal role in the regulation of this process. Members of this family can be either anti-apoptotic, such as Bcl-2, Bcl-xL, Bcl-w, and Mcl-1 in humans, promoting cell survival, or pro-apoptotic, like Bax and Bak, promoting apoptosis and maintaining the balance of cell death and survival.

## Aim of the Project

Our goal is to pioneer a novel approach for protein identification and characterization, utilizing persistent homology—a mathematical framework from Topological Data Analysis (TDA). This method transcends traditional sequence alignment and statistical modeling challenges posed by the diversity of BCL2 sequences across species.

## Significance of BCL2 Proteins

BCL2 proteins exhibit conserved patterns, including similar motifs, common intron positions, a transmembrane segment, characteristic hydrophobic profiles, and relatively conserved three-dimensional structures. These traits are utilized to validate BCL2 proteins post-identification using classical approaches like BLASTp and Hidden Markov Model profiling.

## Problematic

Traditional methods for identifying and classifying protein families are often complex and time-consuming. Our project introduces an innovative perspective by applying persistent homology to compute and analyze the topological features of protein structures represented as three-dimensional point clouds. By encoding these features into barcodes and employing distance measures like the Wasserstein distance, we can compare protein structures without sequence alignment.

## Project Overview

The research encompasses two distinct stages:

1. **Evaluation and Selection of Protein Structures:**
   We use sequences from our Reference Proteome to predict and evaluate 3D structures of BCL2 proteins using AlphaFold2. We focus on high-confidence structures to ensure the quality and reliability of subsequent analyses.

2. **Topological Data Analysis:**
   TDA, particularly persistent homology, is utilized to gain insights into the topology of BCL2 proteins. We automate the generation of barcodes for each structure and create a Wasserstein distance matrix, distributing these distances in a density plot to identify ranges that indicate significant structural similarity and a heatmap to visualize the pairwise distances between structures, revealing clusters and patterns of similarity within the protein family.

## Conclusion

The project endeavors to enhance the methods for protein family identification and classification. By adopting a topological perspective, we aim to add a new dimension to bioinformatics analyses, providing a more nuanced understanding of protein structure and function relationships.
