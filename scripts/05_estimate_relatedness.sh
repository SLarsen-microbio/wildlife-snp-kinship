#!/usr/bin/env bash
set -euo pipefail

# Estimate pairwise genetic relatedness among deer.
#
# Input: LD-pruned PLINK dataset
# Software: PLINK 1.9 and PLINK 2.0
#
# KING-robust kinship coefficients provide candidate
# relationship estimates.
#
# PLINK --genome estimates Z0, Z1, Z2 and PI_HAT.
# These estimates are exploratory and may be affected
# by population structure and marker characteristics.

INPUT="data/processed/deer_kinship"
OUTDIR="results/kinship"

mkdir -p "$OUTDIR"

# KING-robust pairwise kinship estimates.
plink2 \
    --bfile "$INPUT" \
    --allow-extra-chr \
    --make-king-table \
    --out "$OUTDIR/deer_king"

# PLINK identity-by-descent estimates.
plink \
    --bfile "$INPUT" \
    --allow-extra-chr \
    --genome \
    --out "$OUTDIR/deer_ibd"

# Generate candidate-relative network and visualization.
python scripts/build_kinship_network.py

echo "Relatedness analysis complete."
