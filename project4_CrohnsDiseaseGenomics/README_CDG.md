# Integrative Multi-omic Approaches to Characterization of Crohn’s Disease Immune Profiles in Peripheral Blood Mononuclear Cells
This project explores the immune dysregulation present in Inflammatory Bowel Disease (IBD), specifically Crohn's Disease, by analyzing multi-omics data from peripheral blood mononuclear cells (PBMCs). The study aims to determine distinct transcription factor binding and gene expression profiles in PBMCs of Crohn's Disease patients compared to healthy controls. Using snATAC-seq and snRNA-seq data, this study employs a comprehensive analysis pipeline to reveal genetic and epigenetic influences on immune activity and gene expression in Crohn's Disease.

## Completion Date
March 31, 2025

# Installation
To replicate or further develop the analysis conducted in this project, ensure that you have the following requirements in your development environment:

Access to dataset from the National Library of Medicine National Center for Biotechnology Information SRA Lookup.
R version 4.5 or later for snRNA-seq data analysis.
Seurat package version 5.2.1 for single-nucleus RNA sequencing data processing.
Nextflow version compatible with snATACseq-NextFlow for snATAC-seq data processing.
Bioinformatics tools like fastQC, BWA, MACS2, and ataqv for ATAC-seq analysis.
ggplot2 for visualization.

# Usage
Clone the repository containing the analysis scripts:
git clone https://github.com/watsonnikki/CrohnsDiseaseGenomics.git

Install the required R packages and bioinformatics tools as listed under "Installation".

Download the raw data by following these steps:

Utilize the SRA Toolkit to retrieve seq data using the query string given in the methods section.
Follow the specific pipeline instructions mentioned in the study for quality control and analysis of each data type:

For snATAC-seq, adapt snATACseq-NextFlow pipeline for analysis steps.
For snRNA-seq, use the Seurat package for quality control, normalization, and clustering analysis task.
Utilize provided scripts to recreate figures and results documented in the project. Modify parameters and input files according to your datasets as necessary.

# Coding style
The technologies and tools used in this project include:

R and R packages (Seurat, Bioconductor, ggplot2)

Seurat: https://satijalab.org/seurat/
Bioconductor: https://www.bioconductor.org/
Nextflow for workflow management: https://www.nextflow.io/

Bioinformatics tools for ATAC-seq analysis:

snATACseq-NextFlow: https://github.com/porchard/snATACseq-NextFlow.git
fastQC: http://www.bioinformatics.babraham.ac.uk/projects/fastqc/
BWA: http://bio-bwa.sourceforge.net/
MACS2: https://github.com/macs3-project/MACS
Dataset queries and retrieval:

SRA Toolkit: https://ncbi.github.io/sra-tools/

