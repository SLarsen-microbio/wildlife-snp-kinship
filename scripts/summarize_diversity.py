#!/usr/bin/env python3
"""Summarize heterozygosity-based F estimates and visualize PCA."""

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

diversity_dir = Path("results/diversity")
pca_dir = Path("results/pca")
figure_dir = Path("figures/diversity")

figure_dir.mkdir(parents=True, exist_ok=True)

# Load heterozygosity estimates.
het = pd.read_csv(
    diversity_dir / "deer_heterozygosity.het",
    sep=r"\s+"
)

het["Deer"] = het["FID"].astype(str) + "_" + het["IID"].astype(str)

# Export summary statistics.
summary = het["F"].describe()
summary.to_csv(diversity_dir / "f_summary.csv", header=["F"])

het[["Deer", "F"]].sort_values(
    "F", ascending=False
).to_csv(
    diversity_dir / "individual_f_estimates.csv",
    index=False
)

print("Individual F summary:")
print(summary)

# Histogram of F estimates.
plt.figure(figsize=(8, 5))
plt.hist(het["F"], bins=20, edgecolor="black")
plt.xlabel("Heterozygosity-based F estimate")
plt.ylabel("Number of deer")
plt.title("Distribution of Individual F Estimates")
plt.tight_layout()
plt.savefig(
    figure_dir / "deer_f_distribution.png",
    dpi=300
)
plt.close()

# Load PCA coordinates.
pca = pd.read_csv(
    pca_dir / "deer_pca.eigenvec",
    sep=r"\s+",
    header=None
)

pca.columns = [
    "FID", "IID"
] + [
    f"PC{i}" for i in range(1, len(pca.columns) - 1)
]

pca["Deer"] = (
    pca["FID"].astype(str) + "_" + pca["IID"].astype(str)
)

# Export labeled PCA coordinates.
pca.to_csv(
    pca_dir / "deer_pca_coordinates.csv",
    index=False
)

# Plot PC1 versus PC2.
plt.figure(figsize=(8, 6))
plt.scatter(
    pca["PC1"],
    pca["PC2"],
    alpha=0.75
)

plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.title("Genetic Variation Among Sitka Black-Tailed Deer")
plt.tight_layout()

plt.savefig(
    figure_dir / "deer_pca.png",
    dpi=300
)
plt.close()

print(f"\nPCA individuals: {len(pca)}")
print("Saved diversity summaries and figures.")
