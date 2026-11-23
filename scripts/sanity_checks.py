from src.tools.stats import load_matches, head_to_head, win_rate, grand_slam_record, serve_stats, recent_form, top_players
df = load_matches()

# print("rows:", len(df))
# print(df[["winner_name", "loser_name", "surface", "year"]].head())

# print(df["surface"].value_counts(dropna=False))
# print("years:", df["year"].min(), "to", df["year"].max())

# print(win_rate(df, "Rafael Nadal", surface="Clay"))
# print(win_rate(df, "Rafael Nadal", surface="Grass"))

# print(head_to_head(df, "Rafael Nadal", "Roger Federer"))

# print(grand_slam_record(df, "Rafael Nadal"))

# print(serve_stats(df, "Rafael Nadal"))
# print(serve_stats(df, player= "John Isner"))

# print(recent_form(df, "Rafael Nadal", n=5))

print(top_players(df, surface="Clay", year=2019, n=5))