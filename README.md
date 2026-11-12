# Wildlife SNP Analysis Framework

## Project Overview

This repository presents a modular, reproducible bioinformatics framework for analyzing SNP-based wildlife genetic data.

The framework demonstrates genotype quality control, genetic diversity assessment, population structure analysis, pairwise relatedness estimation, and visualization of candidate genetic relationships using graph-based methods.

Publicly available RADseq-derived SNP data from Sitka black-tailed deer (*Odocoileus hemionus sitkensis*) are used as a demonstration dataset.

**This is an analytical demonstration framework, not a completed population-genetics study or a validated production pipeline.**

The objective is to demonstrate computational approaches and scientific reasoning applicable to wildlife genetics. Individual components may be adapted to other species and research questions with appropriate validation.

## Framework Objectives

1. Assess genotype completeness and data quality.
2. Apply reproducible SNP and individual filtering procedures.
3. Examine genetic diversity and population structure.
4. Estimate pairwise genetic relatedness.
5. Evaluate candidate relationships using kinship and identity-by-descent statistics.
6. Construct and visualize genetic relationship networks.
7. Document analytical assumptions, limitations, and opportunities for further development.

## Dataset and Provenance

### Original Study

The demonstration dataset originates from:

Burgess, Irvine, and Russello (2022). *Population genomics of Sitka black-tailed deer supports invasive species management and ecological restoration on islands.* Communications Biology, 5, 223.
https://www.nature.com/articles/s42003-022-03159-5

The study investigated genetic connectivity among invasive Sitka black-tailed deer populations across the Haida Gwaii archipelago in British Columbia, Canada.

### Independent Demonstration

This framework was developed independently using publicly available genetic data originally generated and published by Burgess et al. (2022).

The original researchers conducted the field sampling, laboratory work, sequencing, and upstream bioinformatics processing. The analyses presented in this repository begin with the deposited VCF and demonstrate an independently developed workflow for SNP quality control, genetic diversity assessment, relatedness estimation, and network visualization.

This project is not affiliated with the original research team and does not attempt to reproduce or validate all findings of the published study.

### Original Data Processing

The original researchers performed the upstream laboratory and bioinformatics processing, including:

- RADseq library preparation and Illumina sequencing.
- Read demultiplexing and quality filtering.
- PCR duplicate removal.
- Alignment to a mule deer reference genome using BWA-MEM.
- SNP discovery and genotyping using Stacks.
- Filtering based on locus completeness and minor allele frequency.
- Retention of one SNP per RAD locus to reduce linkage.
- Removal of identified outlier loci and loci showing substantial Hardy–Weinberg disequilibrium.

The published study reports a final analytical dataset of 181 individuals and 12,947 neutral SNPs.

### Input Data for This Framework

This repository begins with the publicly deposited VCF rather than raw sequencing reads.

Link: https://datadryad.org/dataset/doi%253A10.5061/dryad.q2bvq83mq?utm
Initial VCF characteristics:

| Characteristic | Value |
|---|---|
| Species | Sitka black-tailed deer |
| Data type | RADseq-derived SNP genotypes |
| Individuals | 182 |
| Reported sampling populations | 15 |
| Variant records | 12,961 |
| Format | VCF |
| Upstream variant calling | Stacks v2.41 |

The original VCF is retained locally without modification.

The additional filtering and analyses described below were performed independently for this demonstration. They do not reproduce the original study's complete analytical workflow.

## Software

The framework was developed using:

- Python 3.11
- BCFtools 1.25
- VCFtools 0.1.17
- PLINK 1.9
- PLINK 2.0
- pandas
- NumPy
- NetworkX
- matplotlib

## Analysis Workflow

### 1. Genotype Quality Assessment

Individual and SNP missingness, allele frequencies, and heterozygosity-related statistics were evaluated using VCFtools.

Thirteen individuals exceeded the selected maximum genotype missingness threshold of 20%.

### 2. SNP Filtering and Preparation

Filtering criteria included:

- Maximum individual missingness: 20%.
- Maximum SNP missingness: 10%.
- Minimum minor allele frequency: 0.05.

The original VCF required additional header preparation because reference contig declarations were absent.

BCFtools was used to prepare, sort, compress, and index the genotype data.

PLINK was used to convert the filtered VCF to binary genotype format and perform linkage disequilibrium pruning.

The resulting datasets were:

| Processing stage | Individuals | SNPs |
|---|---:|---:|
| Original VCF | 182 | 12,961 |
| Missingness filtering | 169 | 12,947 |
| MAF filtering | 169 | 10,815 |
| LD pruning | 169 | 6,461 |

The matching 12,947 SNP count in the published study and this framework results from different filtering procedures and does not establish equivalence between the datasets.

### 3. Genetic Diversity and Population Structure

Individual heterozygosity-based F estimates were calculated using PLINK.

Principal component analysis was performed using the LD-pruned genotype dataset to examine patterns of genetic variation.

The F estimates varied substantially among individuals, and the PCA revealed pronounced differentiation among subsets of deer.

Because individuals originated from potentially differentiated populations, pooled allele frequencies may influence heterozygosity-based F estimates.

These statistics are therefore interpreted as exploratory measures of homozygosity relative to the analyzed sample, not definitive evidence of recent inbreeding.

### 4. Pairwise Genetic Relatedness

KING-robust kinship coefficients were estimated using PLINK 2.0.

PLINK 1.9 was additionally used to estimate identity-by-descent statistics, including Z0, Z1, Z2, and PI_HAT.

IBS0 values were examined to provide additional information about candidate close-relative relationships.

The framework identified 128 candidate relative pairs using selected kinship thresholds:

| Candidate relationship category | Pairs |
|---|---:|
| First-degree | 29 |
| Second-degree | 45 |
| Third-degree | 54 |
| Total | 128 |

These classifications represent candidate relationships, not confirmed pedigree assignments.

### 5. Genetic Relationship Networks

Candidate relationships were represented using an undirected NetworkX graph.

Individuals are represented as nodes, and candidate genetic relationships are represented as edges.

The resulting network contains:

- 67 individuals with at least one candidate relationship.
- 128 edges.
- 10 connected components.

The network is exported in GEXF format and visualized as a PNG figure.

Connected components should not be interpreted as confirmed family groups.

## Reproducible Workflow

The analytical workflow is organized into sequential scripts:

```text
scripts/
├── 01_initial_qc.sh
├── 02_filter_missingness.sh
├── 03_prepare_vcf.sh
├── 04_prepare_plink.sh
├── 05_estimate_relatedness.sh
├── 06_genetic_diversity.sh
├── build_kinship_network.py
├── compare_relatedness.py
├── summarize_diversity.py
└── summarize_sample_groups.py
```

The six numbered shell scripts implement the primary analytical stages.

The Python scripts provide additional summaries, comparisons, and visualizations.

### Execution Order

After obtaining the original VCF and installing the required software, run the following commands from the repository root:

```bash
bash scripts/01_initial_qc.sh
bash scripts/02_filter_missingness.sh
bash scripts/03_prepare_vcf.sh
bash scripts/04_prepare_plink.sh
bash scripts/05_estimate_relatedness.sh
bash scripts/06_genetic_diversity.sh

python scripts/compare_relatedness.py
python scripts/summarize_diversity.py
```

The kinship network script is called by `05_estimate_relatedness.sh`.

The workflow is being prepared for end-to-end reproducibility verification. The documented output counts represent the completed exploratory analyses.

## Outputs

Selected analytical outputs include:

```text
results/
├── qc/
├── ld/
├── kinship/
├── diversity/
└── pca/

figures/
├── kinship/
└── diversity/
```

Principal visualizations include:

- `figures/kinship/deer_kinship_network.png`
- `figures/diversity/deer_f_distribution.png`
- `figures/diversity/deer_pca.png`

Detailed analytical decisions and troubleshooting notes are maintained in `docs/analysis_log.md`.

## Framework Limitations

This repository is intended to demonstrate selected computational methods rather than provide definitive biological or management conclusions.

Important considerations include:

- Population structure may affect kinship estimates and heterozygosity-based statistics.
- The deposited RADseq SNP dataset provides incomplete genomic coverage.
- Kinship thresholds identify candidate relationships but do not establish parentage or complete pedigrees.
- Identity-by-descent estimates depend on model assumptions and genotype characteristics.
- The genetic relationship network is not a validated pedigree.
- Population assignments and geographic connectivity have not been independently reconstructed in this framework.
- Filtering thresholds and analytical parameters require reassessment before application to additional datasets.

## Potential Extensions

The framework could be extended to include population-aware allele frequency estimation, formal pedigree reconstruction, additional population-genetic analyses, or species-specific management applications.

Such extensions would require appropriate metadata, analytical validation, and consideration of the biological questions being investigated.

## Project Status

**Demonstration analyses completed; end-to-end workflow validation and repository documentation in progress.**

The current framework includes SNP quality control, filtering, PCA, heterozygosity analysis, pairwise relatedness estimation, IBD comparisons, and graph-based visualization.

The repository is intended as a modular foundation for further development rather than a comprehensive wildlife population-genetics investigation.
