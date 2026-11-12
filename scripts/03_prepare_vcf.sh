#!/usr/bin/env bash
set -euo pipefail

# Repair missing contig declarations, extract biallelic SNPs,
# sort variants, and create a compressed/indexed VCF.
#
# Requires BCFtools 1.25 and Python 3.

INPUT="data/processed/deer_qc.recode.vcf"
OUTDIR="data/processed"

mkdir -p "$OUTDIR"

# Generate a complete replacement header.
python - "$INPUT" "$OUTDIR/deer_header_fixed.txt" <<'PY'
import sys

input_vcf, output_header = sys.argv[1:3]

metadata = []
chrom_header = None
contigs = set()

with open(input_vcf) as handle:
    for line in handle:
        if line.startswith("##"):
            if not line.startswith("##contig="):
                metadata.append(line)
        elif line.startswith("#CHROM"):
            chrom_header = line
        else:
            contigs.add(line.split("\t", 1)[0])

if chrom_header is None:
    raise ValueError("VCF column header not found")

with open(output_header, "w") as out:
    out.writelines(metadata)

    for contig in sorted(contigs):
        out.write(f"##contig=<ID={contig}>\n")

    out.write(chrom_header)

print(f"Generated header with {len(contigs)} contigs")
PY

# Apply repaired header without modifying the original input.
bcftools reheader \
    -h "$OUTDIR/deer_header_fixed.txt" \
    -o "$OUTDIR/deer_header_repaired.vcf" \
    "$INPUT"

# Retain biallelic SNPs and sort by genomic coordinates.
bcftools view \
    -m2 -M2 -v snps \
    "$OUTDIR/deer_header_repaired.vcf" \
    -Ou |
bcftools sort \
    -Oz \
    -o "$OUTDIR/deer_snps_sorted.vcf.gz"

# Index the sorted VCF.
bcftools index \
    -t \
    "$OUTDIR/deer_snps_sorted.vcf.gz"

echo "VCF preparation complete."
