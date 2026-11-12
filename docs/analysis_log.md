# Analysis Log

## Project Initialization

### Objective

Develop a reproducible SNP-based wildlife genetics workflow demonstrating quality control, kinship estimation, and genetic relationship analysis.

### Input Dataset

File: `deer_182ind_15pop_12961snp.vcf`

Initial dataset characteristics:

- 182 individuals
- 12,961 variant records
- 15 sampling sites
- Generated using Stacks v2.41

The original VCF is retained without modification.
The original study's final neutral SNP dataset contained 181 individuals and 12,947 SNPs. The 12,947 SNPs retained after missingness filtering in this demonstration were obtained using different filtering criteria and should not be assumed to represent the same marker set.

### Software Environment

Conda environment: `wildlife_genetics`

Installed software:

- Python 3.11.18
- BCFtools 1.25
- VCFtools 0.1.17
- PLINK 1.9
- PLINK 2.0

### Baseline Quality Assessment

The following VCFtools analyses were performed:

```bash
vcftools --vcf data/raw/deer_182ind_15pop_12961snp.vcf \
  --missing-indv --out results/qc/deer_baseline

vcftools --vcf data/raw/deer_182ind_15pop_12961snp.vcf \
  --missing-site --out results/qc/deer_baseline

vcftools --vcf data/raw/deer_182ind_15pop_12961snp.vcf \
  --freq2 --out results/qc/deer_baseline

vcftools --vcf data/raw/deer_182ind_15pop_12961snp.vcf \
  --het --out results/qc/deer_baseline
```

### Initial Observations

Individual missingness varied substantially.

Thirteen of 182 individuals (7.1%) had greater than 20% missing genotypes.

The highest missingness values were:

| Individual | Missingness |
|---|---:|
| loui_01 | 51.30% |
| burn_01 | 48.56% |
| hous_01 | 33.23% |
| wlou_x3 | 28.15% |
| lyel_10 | 26.83% |

Several individuals also showed elevated positive genotype-based F estimates.

These estimates cannot be interpreted as direct evidence of recent inbreeding without considering population structure and genotype quality.

### Sample Identifier Investigation

An exploratory analysis grouped individuals by sample-name prefix.

However, the VCF contains inconsistent naming conventions, and the prefixes have not been verified as geographic identifiers.

Decision: Do not infer sampling locations from sample names.

### Preliminary Filtering Strategy

Candidate thresholds:

- Maximum individual missingness: 20%
- Maximum SNP missingness: 10%

Rationale: Establish a reasonably complete genotype dataset for demonstration purposes while preserving sufficient individuals and markers for kinship analysis.

These thresholds were selected as initial demonstration parameters. The resulting sample and marker retention were evaluated after filtering. Their suitability for other datasets would require independent assessment.

### Troubleshooting

An initial VCFtools command included the unsupported option `--max-indv-meanDP`.

The option was removed because depth-based individual filtering was not required for this step.

### Individual Missingness Filtering

**Filtering criterion:** Exclude individuals with greater than 20% missing genotypes.

**Results:**
- Starting individuals: 182
- Excluded individuals: 13
- Retained individuals: 169
- Retained SNP records before additional site filtering: 12,961

After excluding individuals with high missingness, SNP completeness was recalculated.

Fourteen SNPs exceeded 10% missingness in the reduced dataset.

**Decision:** Reapply the 90% SNP completeness threshold after individual filtering.

**Rationale:** Removing individuals changes the proportion of missing genotypes at each locus. Recalculating SNP missingness ensures the final dataset satisfies the selected completeness criterion.

These thresholds are intended for a demonstration pipeline and are not presented as universally optimal for wildlife kinship analysis.

### VCF Header Compatibility

During biallelic SNP extraction, BCFtools reported warnings indicating that reference contig identifiers were not defined in the VCF header.

The original Stacks-generated VCF did not contain `##contig` declarations.

A revised VCF header containing 2,998 contig declarations was generated using the reference sequence identifiers present in the dataset.

The modified VCF was prepared for downstream analysis using BCFtools. The original deposited VCF was preserved unchanged.

End-to-end verification of the automated VCF preparation script remains pending.

## Downstream SNP Analyses

### Minor Allele Frequency Filtering

**Software:** VCFtools 0.1.17

A minor allele frequency threshold of 0.05 was applied to the missingness-filtered dataset.

**Results:**

- Starting individuals: 169
- Starting SNPs: 12,947
- SNPs retained after MAF filtering: 10,815

The MAF threshold was selected for this demonstration and is not assumed to be optimal for all wildlife genetics applications.

### Linkage Disequilibrium Pruning

**Software:** PLINK 1.9

LD pruning was performed using:

plink \
  --bfile data/processed/deer_plink \
  --allow-extra-chr \
  --indep-pairwise 50 5 0.2 \
  --out results/ld/deer_ld

**Results:**

- SNPs before LD pruning: 10,815
- SNPs retained after pruning: 6,461

The LD-pruned dataset was used for PCA and KING relatedness estimation.

Because the RADseq dataset contains numerous short reference contigs and was originally filtered to retain one SNP per RAD locus, conventional LD-pruning windows may not correspond directly to physical genomic distances.

### Pairwise Relatedness Estimation

**Software:** PLINK 2.0

KING-robust kinship coefficients were calculated for the 169 retained individuals.

**Results:**

- Individuals: 169
- Pairwise comparisons: 14,196
- Candidate first-degree pairs: 29
- Candidate second-degree pairs: 45
- Candidate third-degree pairs: 54
- Total candidate relative pairs: 128

The classifications used conventional KING kinship coefficient thresholds.

These estimates are used for exploratory relationship screening and should not be interpreted as confirmed pedigree relationships.

Population structure may affect kinship estimation, particularly when genetically differentiated populations are analyzed together.

### Identity-by-Descent Comparisons

**Software:** PLINK 1.9

PLINK's pairwise IBD analysis was used to estimate:

- **Z0:** Estimated probability of sharing zero alleles identical by descent at a locus.
- **Z1:** Estimated probability of sharing one allele identical by descent at a locus.
- **Z2:** Estimated probability of sharing two alleles identical by descent at a locus.
- **PI_HAT:** Estimated proportion of the genome shared identical by descent, calculated as Z2 + 0.5 × Z1.

The 128 candidate relative pairs identified through KING were matched to their corresponding PLINK IBD estimates.

For the 29 first-degree candidate pairs, approximate IBS0 counts were calculated by multiplying the KING-reported IBS0 proportion by the number of SNPs evaluated for each pair and rounding to the nearest integer.

| Statistic | IBS0 count |
|---|---:|
| Mean | 37.52 |
| Median | 35 |
| Minimum | 7 |
| Maximum | 72 |

These values provide additional information for evaluating candidate relationships but do not independently confirm parentage or distinguish all possible pedigree relationships.

### Genetic Relationship Network

**Software:** Python, NetworkX

Candidate relative pairs were represented as an undirected graph.

**Results:**

- Individuals represented in the candidate relationship network: 67
- Candidate relationship edges: 128
- Connected components: 10
- Largest connected component: 25 individuals

The network illustrates how graph-based methods can organize candidate genetic relationships.

Edges represent estimated relatedness, not validated pedigree connections.

### Heterozygosity-Based F Estimates

**Software:** PLINK 1.9

Individual F estimates were calculated using the MAF-filtered genotype dataset.

**Results:**

| Statistic | Value |
|---|---:|
| Individuals | 169 |
| Mean F | 0.137 |
| Median F | 0.075 |
| Minimum F | −0.262 |
| Maximum F | 0.620 |

Seven of the ten individuals with the highest F estimates shared the `sgan` sample identifier prefix.

Because the analysis used pooled allele frequencies from potentially differentiated populations, these estimates cannot be interpreted directly as evidence of recent inbreeding.

The sample prefixes have not been independently validated as geographic identifiers.

### Principal Component Analysis

**Software:** PLINK 1.9, Python

PCA was performed using 6,461 LD-pruned SNPs from 169 individuals.

The resulting visualization showed pronounced differentiation between subsets of individuals.

This observation indicates that population structure should be considered when interpreting pairwise relatedness and heterozygosity-based statistics.

Sample-to-population assignments have not yet been independently verified.

### Interpretation and Scope

These analyses demonstrate a modular workflow for processing SNP genotype data, evaluating genetic diversity, estimating candidate relationships, and visualizing genetic patterns.

The results are exploratory and are not intended to reproduce the original study's findings or establish definitive biological conclusions.

The workflow does not currently include formal pedigree reconstruction, population-specific kinship calibration, or migration modeling.

### Reproducibility Status

The analytical components have been executed during development, and their results are documented above.

The sequential shell scripts have been assembled but have not yet undergone a complete clean, end-to-end execution test.

Reproducibility verification remains a required step before presenting the framework as fully tested.
