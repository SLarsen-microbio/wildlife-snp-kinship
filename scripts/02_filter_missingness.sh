#!/usr/bin/env bash
set -euo pipefail

# Wildlife SNP kinship project
# Filter individuals and SNPs based on genotype missingness.
#
# Requirements:
#   VCFtools 0.1.17
#   Python 3 with pandas
#
# Thresholds:
#   Individual missingness > 0.20: exclude
#   SNP missingness > 0.10: exclude

INPUT="data/raw/deer_182ind_15pop_12961snp.vcf"
OUTDIR="data/processed"
QCDIR="results/qc"

mkdir -p "$OUTDIR" "$QCDIR"

# Step 1: Initial SNP missingness filtering.
vcftools \
    --vcf "$INPUT" \
    --max-missing 0.90 \
    --recode \
    --recode-INFO-all \
    --out "$OUTDIR/deer_site_filtered"

# Step 2: Calculate individual missingness on the filtered VCF.
vcftools \
    --vcf "$OUTDIR/deer_site_filtered.recode.vcf" \
    --missing-indv \
    --out "$QCDIR/deer_site_filtered"

# Step 3: Generate individual exclusion list.
python - <<'PY'
import pandas as pd
from pathlib import Path

input_file = Path("results/qc/deer_site_filtered.imiss")
output_file = Path("data/processed/exclude_high_missingness.txt")

df = pd.read_csv(input_file, sep=r"\s+")

excluded = df.loc[df["F_MISS"] > 0.20, "INDV"]

excluded.to_csv(output_file, index=False, header=False)

print(f"Excluded individuals: {len(excluded)}")
PY

# Step 4: Remove individuals exceeding missingness threshold.
vcftools \
    --vcf "$OUTDIR/deer_site_filtered.recode.vcf" \
    --remove "$OUTDIR/exclude_high_missingness.txt" \
    --recode \
    --recode-INFO-all \
    --out "$OUTDIR/deer_filtered"

# Step 5: Reapply SNP missingness threshold.
vcftools \
    --vcf "$OUTDIR/deer_filtered.recode.vcf" \
    --max-missing 0.90 \
    --recode \
    --recode-INFO-all \
    --out "$OUTDIR/deer_qc"

echo "Missingness filtering complete."
