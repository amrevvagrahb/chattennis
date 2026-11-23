from src.tools.stats import load_matches, head_to_head, win_rate
df = load_matches()

# print("rows:", len(df))
# print(df[["winner_name", "loser_name", "surface", "year"]].head())

# print(df["surface"].value_counts(dropna=False))
# print("years:", df["year"].min(), "to", df["year"].max())

# print(win_rate(df, "Rafael Nadal", surface="Clay"))
# print(win_rate(df, "Rafael Nadal", surface="Grass"))

print(head_to_head(df, "Rafael Nadal", "Roger Federer"))