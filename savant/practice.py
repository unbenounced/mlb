# %%
from __future__ import annotations

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
regular_season = sav.loc[sav["game_type"] == "R"]

# %%
slashline = regular_season.groupby(["batter_name", "batter"])[["is_atbat", "is_hit"]].sum().reset_index()
slashline.head()

# %%

slashline["avg"] = round(slashline["is_hit"] / slashline["is_atbat"], 3)
slashline_filtered = slashline[slashline["is_atbat"] > 100].sort_values(by="avg", ascending=False)
slashline_filtered.head()
# %%
# %%
slashline.loc[slashline["batter"] == 701762]
# %%
slashline.head()
# %%
# xwOBA, xBA, xSLG, avg_exit_velo, barrel_pct, hard_hit_pct, la_sweet_spot_pct, bat_speed, squared_up_pct, chase_pct, whiff_pct, k_pct, bb_pct

def batting_stats(sav: pd.DataFrame) -> pd.DataFrame:
