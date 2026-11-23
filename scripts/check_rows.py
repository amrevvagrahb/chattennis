from src.tools.stats import load_matches
df = load_matches()
print("rows:", len(df))
print(df[["winner_name", "loser_name", "surface", "year"]].head())