from src.tools.stats import load_matches
df = load_matches()
print(df["surface"].value_counts(dropna=False))
print("years:", df["year"].min(), "to", df["year"].max())