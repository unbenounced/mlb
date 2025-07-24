# %%
from pathlib import Path

import pandas as pd
import numpy as np

pd.set_option('display.max_columns', 500)

DATA_DIR = Path("data")
if not DATA_DIR.exists():
  DATA_DIR = Path("savant/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

sav = pd.read_csv(DATA_DIR / "add_ons.csv")

# %%
pg = sav.loc[sav["game_pk"] == 777063].sort_values(by=["at_bat_number", "pitch_number"])
# %%
pg.head()
# %%
pg = pg[["batter_name", "pitcher_name", "on_3b", "on_2b", "on_1b", "outs_when_up", "inning", "at_bat_number", "pitch_number"]]
# %%
pg.loc[(pg["batter_name"] == "Max Kepler") & (pg["inning"] == 10) & (pg["des"].str.contains("intentionally walks", na=False))]
# %%
iw = sav.loc[sav["des"].str.contains("intentionally walks", na=False)]
# %%
iw.sort_values
# %%
iw["events"].value_counts()
# %%
# intentional walk
sav.loc[(sav["events"].isna().sum()) & (sav["des"].str.contains("intentionally walks", na=False)) & (sav["pitch_number"]  == 1)]
# %%
