#!/usr/bin/env python3
"""Compare KING candidate relatives with PLINK IBD estimates."""

from pathlib import Path
import pandas as pd

kinship_file = Path("results/kinship/candidate_relatives.csv")
ibd_file = Path("results/kinship/deer_ibd.genome")
output_file = Path("results/kinship/relatedness_comparison.csv")

kinship = pd.read_csv(kinship_file)
ibd = pd.read_csv(ibd_file, sep=r"\s+")

# Construct individual identifiers consistently.
ibd["Deer1"] = ibd["FID1"].astype(str) + "_" + ibd["IID1"].astype(str)
ibd["Deer2"] = ibd["FID2"].astype(str) + "_" + ibd["IID2"].astype(str)

# Pair order is arbitrary; use order-independent identifiers.
def pair_key(a, b):
    return tuple(sorted((str(a), str(b))))

kinship["pair_key"] = [
    pair_key(a, b)
    for a, b in zip(kinship["Deer1"], kinship["Deer2"])
]

ibd["pair_key"] = [
    pair_key(a, b)
    for a, b in zip(ibd["Deer1"], ibd["Deer2"])
]

# Retain relevant IBD estimates.
ibd_subset = ibd[
    ["pair_key", "Z0", "Z1", "Z2", "PI_HAT"]
]

comparison = kinship.merge(
    ibd_subset,
    on="pair_key",
    how="left",
    validate="one_to_one"
)
missing = comparison["PI_HAT"].isna().sum()

if missing:
    raise ValueError(
        f"{missing} candidate relative pairs have no matching IBD estimate."
    )
comparison = comparison.drop(columns=["pair_key"])

# Approximate number of opposite-homozygote SNPs.
comparison["IBS0_count"] = (
    comparison["IBS0"] * comparison["NSNP"]
).round().astype(int)

comparison.to_csv(output_file, index=False)

print("Candidate relative pairs:", len(comparison))
print("Pairs with IBD estimates:", comparison["PI_HAT"].notna().sum())

print("\nCandidate relationship categories:")
print(comparison["Relationship"].value_counts())

print("\nFirst-degree candidate IBS0 counts:")
print(
    comparison.loc[
        comparison["Relationship"] == "First-degree",
        "IBS0_count"
    ].describe()
)

print(f"\nSaved: {output_file}")
