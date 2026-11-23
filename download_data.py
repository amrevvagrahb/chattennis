from pathlib import Path
from urllib.request import urlretrieve
from urllib.error import HTTPError

BASE = "https://raw.githubusercontent.com/Aneeshers/tennis-sackmann-archive/main/atp"
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

for year in range(2000, 2025):
    name = f"atp_matches_{year}.csv"
    dest = DATA_DIR / name
    if dest.exists():
        print(f"skip {name} (already there)")
        continue
    try:
        urlretrieve(f"{BASE}/{name}", dest)
        print(f"ok   {name}")
    except HTTPError as e:
        print(f"FAIL {name}: HTTP {e.code}")