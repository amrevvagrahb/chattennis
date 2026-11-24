from src.tools.stats import load_matches, head_to_head, win_rate, grand_slam_record, serve_stats, recent_form, top_players
from src.tools.stats_tools import win_rate_tool
from collections import Counter
from src.ingest import load_pages, chunk_pages

# df = load_matches()

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

# print(top_players(df, surface="Clay", year=2019, n=5))

# print(win_rate_tool('murray'))

# pages= load_pages()
# print(Counter(p["source"] for p in pages))
# print(pages[0]["text"][:300])

chunks = chunk_pages(load_pages())
print("chunks:", len(chunks))
print(chunks[10])