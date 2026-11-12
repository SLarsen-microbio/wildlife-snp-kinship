#!/usr/bin/env python3

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

# Paths
input_file = Path("results/kinship/deer_king.kin0")
output_dir = Path("results/kinship")
figure_dir = Path("figures/kinship")

output_dir.mkdir(parents=True, exist_ok=True)
figure_dir.mkdir(parents=True, exist_ok=True)

# Load KING results
df = pd.read_csv(input_file, sep=r"\s+")

# Reconstruct individual IDs
df["Deer1"] = df["#FID1"].astype(str) + "_" + df["IID1"].astype(str)
df["Deer2"] = df["FID2"].astype(str) + "_" + df["IID2"].astype(str)

# Classify kinship
def classify_kinship(k):
    if k > 0.354:
        return "Duplicate/identical"
    elif k >= 0.177:
        return "First-degree"
    elif k >= 0.0884:
        return "Second-degree"
    elif k >= 0.0442:
        return "Third-degree"
    else:
        return "Distant/unrelated"

df["Relationship"] = df["KINSHIP"].apply(classify_kinship)

# Export candidate relatives
relatives = df[df["KINSHIP"] >= 0.0442].copy()
relatives = relatives.sort_values("KINSHIP", ascending=False)

relatives.to_csv(
    output_dir / "candidate_relatives.csv",
    index=False
)

# Build network
G = nx.Graph()

for _, row in relatives.iterrows():
    G.add_edge(
        row["Deer1"],
        row["Deer2"],
        kinship=row["KINSHIP"],
        relationship=row["Relationship"]
    )

# Network statistics
components = sorted(
    nx.connected_components(G),
    key=len,
    reverse=True
)

print("Candidate relative pairs:", len(relatives))
print("Deer with candidate relatives:", G.number_of_nodes())
print("Network edges:", G.number_of_edges())
print("Connected components:", len(components))

if components:
    print("Largest connected component:", len(components[0]))

# Save network edges
nx.write_gexf(G, output_dir / "deer_kinship_network.gexf")

# Plot
plt.figure(figsize=(12, 9))

pos = nx.spring_layout(G, seed=42)

colors = {
    "First-degree": "red",
    "Second-degree": "orange",
    "Third-degree": "lightblue",
    "Duplicate/identical": "purple"
}

nx.draw_networkx_nodes(
    G, pos,
    node_size=80,
    node_color="steelblue"
)

for relationship, color in colors.items():
    edges = [
        (u, v)
        for u, v, data in G.edges(data=True)
        if data["relationship"] == relationship
    ]

    nx.draw_networkx_edges(
        G, pos,
        edgelist=edges,
        edge_color=color,
        width=1.5,
        alpha=0.7,
        label=relationship
    )

plt.title("Candidate Genetic Relationships Among Sitka Black-Tailed Deer")
plt.legend()
plt.axis("off")
plt.tight_layout()

plt.savefig(
    figure_dir / "deer_kinship_network.png",
    dpi=300
)

plt.close()
