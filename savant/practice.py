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
# xwOBA, xBA, xSLG, avg_exit_velo, barrel_pct, hard_hit_pct, la_sweet_spot_pct, bat_speed, squared_up_pct, chase_pct, whiff_pct, k_pct, bb_pct

def batting_stats(sav: pd.DataFrame) -> pd.DataFrame:
  out = sav.copy()

  sc = out.groupby(["batter_name", "batter"])[["is_atbat", "is_walk", "is_hit_by_pitch", "is_sac_fly"]].sum().reset_index()

  # Calculate xwOBAcon
  # Filter for only batted balls
  batted_balls = out[out["type"] == "X"]
  # Drop missing xwOBA values
  batted_balls = batted_balls[batted_balls["estimated_woba_using_speedangle"].notna()]
  # Group by batter and sum xwOBA contributions
  xwOBAcon = (
    batted_balls.groupby(["batter_name", "batter"])["estimated_woba_using_speedangle"]
    .sum()
    .reset_index()
    .rename(columns={"estimated_woba_using_speedangle": "xwOBAcon"})
  )

  sc = sc.merge(xwOBAcon, how="left", on=["batter_name", "batter"])

  # Calculate league weight for walks (excluding intential walks)
  total_woba_from_walks = out.loc[out["is_walk"]]["woba_value"].sum()
  num_walks = out["is_walk"].sum()
  wBB = total_woba_from_walks / num_walks

  # Calculate league weight for hit by pitch
  total_woba_from_hbp = out.loc[out["is_hit_by_pitch"]]["woba_value"].sum()
  num_hbp = out["is_hit_by_pitch"].sum()
  wHBP = total_woba_from_hbp / num_hbp

  sc["xwOBA"] = round((sc["xwOBAcon"] + wBB * sc["is_walk"] + wHBP * sc["is_hit_by_pitch"]) / (sc["is_atbat"] + sc["is_walk"] + sc["is_sac_fly"] + sc["is_hit_by_pitch"]), 3)

  return sc
# %%
df = batting_stats(regular_season)
df.head()


# %%
