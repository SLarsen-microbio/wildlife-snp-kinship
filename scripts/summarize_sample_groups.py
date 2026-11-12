import pandas as pd

df = pd.read_csv(
    "results/qc/deer_baseline.imiss",
    sep=r"\s+"
)

# Extract provisional sample group
df["group"] = df["INDV"].str.split("_").str[0]

summary = (
    df.groupby("group")
    .agg(
        n_individuals=("INDV", "count"),
        mean_missingness=("F_MISS", "mean"),
        median_missingness=("F_MISS", "median"),
        max_missingness=("F_MISS", "max"),
        n_over_20pct=("F_MISS", lambda x: (x > 0.20).sum())
    )
    .sort_values("mean_missingness", ascending=False)
)

print(summary.to_string())

summary.to_csv(
    "results/qc/provisional_group_missingness.csv"
)
