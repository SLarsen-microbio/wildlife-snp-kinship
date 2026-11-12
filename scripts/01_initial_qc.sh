#!/usr/bin/env bash
set -euo pipefail

# Initial quality assessment of the original deer SNP dataset.
# Requires VCFtools 0.1.17.

INPUT="data/raw/deer_182ind_15pop_12961snp.vcf"
OUTDIR="results/qc"

mkdir -p "$OUTDIR"

if [[ ! -f "$INPUT" ]]; then
    echo "ERROR: Input VCF not found: $INPUT" >&2
    exit 1
fi

vcftools --vcf "$INPUT" \
    --missing-indv \
    --out "$OUTDIR/deer_baseline"

vcftools --vcf "$INPUT" \
    --missing-site \
    --out "$OUTDIR/deer_baseline"

vcftools --vcf "$INPUT" \
    --freq2 \
    --out "$OUTDIR/deer_baseline"

vcftools --vcf "$INPUT" \
    --het \
    --out "$OUTDIR/deer_baseline"

echo "Initial QC complete."
