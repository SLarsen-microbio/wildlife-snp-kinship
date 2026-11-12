#!/usr/bin/env bash
set -euo pipefail

# Apply MAF filtering, convert to PLINK format,
# and perform LD pruning.
#
# Requires VCFtools 0.1.17 and PLINK 1.9.

INPUT="data/processed/deer_snps_sorted.vcf.gz"
OUTDIR="data/processed"
LDDIR="results/ld"

mkdir -p "$OUTDIR" "$LDDIR"

# Retain SNPs with minor allele frequency >= 0.05.
vcftools \
    --gzvcf "$INPUT" \
    --maf 0.05 \
    --recode \
    --recode-INFO-all \
    --out "$OUTDIR/deer_maf05"

# Convert VCF to PLINK binary format.
plink \
    --vcf "$OUTDIR/deer_maf05.recode.vcf" \
    --allow-extra-chr \
    --make-bed \
    --out "$OUTDIR/deer_plink"

# LD pruning: 50-SNP window, 5-SNP step, r² threshold 0.2.
plink \
    --bfile "$OUTDIR/deer_plink" \
    --allow-extra-chr \
    --indep-pairwise 50 5 0.2 \
    --out "$LDDIR/deer_ld"

# Create LD-pruned genotype dataset.
plink \
    --bfile "$OUTDIR/deer_plink" \
    --allow-extra-chr \
    --extract "$LDDIR/deer_ld.prune.in" \
    --make-bed \
    --out "$OUTDIR/deer_kinship"

echo "PLINK preparation complete."
