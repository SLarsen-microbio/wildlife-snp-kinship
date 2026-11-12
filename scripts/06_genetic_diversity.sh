#!/usr/bin/env bash
set -euo pipefail

# Estimate individual heterozygosity and genetic structure.
#
# Software: PLINK 1.9
#
# Heterozygosity uses the MAF-filtered dataset.
# PCA uses the LD-pruned dataset.

OUTDIR="results/diversity"
PCADIR="results/pca"

mkdir -p "$OUTDIR" "$PCADIR"

# Individual heterozygosity and method-of-moments F.
plink \
    --bfile data/processed/deer_plink \
    --allow-extra-chr \
    --het \
    --out "$OUTDIR/deer_heterozygosity"

# Principal component analysis.
plink \
    --bfile data/processed/deer_kinship \
    --allow-extra-chr \
    --pca 10 \
    --out "$PCADIR/deer_pca"

echo "Genetic diversity analysis complete."
