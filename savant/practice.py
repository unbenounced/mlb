# %%
from __future__ import annotations

from pathlib import Path

import pandas as pd
import numpy as np
import config as cfg
import loader
import processor

loader.main()
processor.main()

pd.set_option('display.max_columns', 500)

DATA_DIR = Path("data")
if not DATA_DIR.exists():
  DATA_DIR = Path("savant/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

add_ons = pd.read_csv(DATA_DIR / "add_ons.csv")

# %%
regular_season = add_ons.loc[add_ons["game_type"] == "R"]

# %%
# [x] xwOBA, [/]xBA, []xSLG, []avg_exit_velo, []barrel_pct, []hard_hit_pct, []la_sweet_spot_pct, []bat_speed, []squared_up_pct, []chase_pct, []whiff_pct, []k_pct, []bb_pct
def get_xwOBA(add_ons_df: pd.DataFrame) -> pd.DataFrame:
  add_ons_copy = add_ons_df.copy()

  # Summarize plate appearance events
  stats_summarized = (
    add_ons_copy.groupby(["batter_name", "batter"])
    .agg({
      "is_atbat": "sum", 
      "is_walk": "sum", 
      "is_hit_by_pitch": "sum", 
      "is_sac_fly": "sum"
    })
    .reset_index()
  )

  # Calculate xwOBAcon
  # Filter for only balls hit in play and with valid xwOBA estimate
  batted_balls = add_ons_copy[
    add_ons_copy["is_ball_in_play"] & 
    (add_ons_copy["estimated_woba_using_speedangle"].notna())
  ]

  # Count balls put in play per batter
  batted_balls_count = (
    batted_balls.groupby(["batter_name", "batter"])
    .size()
    .reset_index(name="batted_balls")
  )

  # Mean xwOBAcon per batter
  xwOBAcon = (
    batted_balls.groupby(["batter_name", "batter"])["estimated_woba_using_speedangle"]
    .mean()
    .reset_index()
    .rename(columns={"estimated_woba_using_speedangle": "xwOBAcon"})
  )

  # Merge into summary stats
  stats_summarized = stats_summarized.merge(xwOBAcon, how="left", on=["batter_name", "batter"])
  stats_summarized = stats_summarized.merge(batted_balls_count, how="left", on=["batter_name", "batter"])

  # Fill missing values
  stats_summarized["xwOBAcon"] = stats_summarized["xwOBAcon"].fillna(0)
  stats_summarized["batted_balls"] = stats_summarized["batted_balls"].fillna(0)

  # Calculate league weights (excluding intentional walks if needed)
  total_woba_from_walks = add_ons_copy.loc[add_ons_copy["is_walk"], "woba_value"].sum()
  num_walks = add_ons_copy["is_walk"].sum()
  wBB = total_woba_from_walks / num_walks if num_walks > 0 else 0

  total_woba_from_hbp = add_ons_copy.loc[add_ons_copy["is_hit_by_pitch"], "woba_value"].sum()
  num_hbp = stats_summarized["is_hit_by_pitch"].sum()
  wHBP = total_woba_from_hbp / num_hbp if num_hbp > 0 else 0

  # Calculate xwOBA
  numerator = (
    stats_summarized["xwOBAcon"] * stats_summarized["batted_balls"] + 
    wBB * stats_summarized["is_walk"] + 
    wHBP * stats_summarized["is_hit_by_pitch"]
  )
  denominator = (
    stats_summarized["is_atbat"] + 
    stats_summarized["is_walk"] + 
    stats_summarized["is_hit_by_pitch"] +
    stats_summarized["is_sac_fly"]
  )
  stats_summarized["xwOBA"] =  numerator / denominator.replace(0, pd.NA)

  return stats_summarized

# %% 
def get_xBA(add_ons_df: pd.DataFrame, xwOBA_df: pd.DataFrame) -> pd.DataFrame:
  add_ons_copy = add_ons_df.copy()

  xstats_df = (
    add_ons_copy.groupby(["batter_name", "batter"])
    .agg(
      xba_sum = ("estimated_ba_using_speedangle", "sum"),
      AB = ("is_atbat", "sum"),
      batted_balls = ("is_ball_in_play", "sum"),
      xslg_sum = ("estimated_slg_using_speedangle", "sum"), 
      exit_velo_sum = ("launch_speed", "mean")
    )
    .reset_index()
  )
  print(xstats_df["exit_velo_sum"])
  xstats_df["xBA"] = xstats_df["xba_sum"] / xstats_df["AB"]
  xstats_df["xSLG"] = xstats_df["xslg_sum"] / xstats_df["AB"]
  xstats_df["avg_exit_velo"] = xstats_df["exit_velo_sum"] / xstats_df["AB"] 

  advanced_stats = xwOBA_df.merge(xstats_df, how="inner", on=["batter_name", "batter"])
  
  return advanced_stats[["batter_name", "batter", "AB", "xBA", "xwOBA", "xSLG", "avg_exit_velo"]]

# %%
def statcast_batting_stats(add_ons_df: pd.DataFrame) -> pd.DataFrame:
  xwOBA = get_xwOBA(add_ons_df)
  xBA = get_xBA(add_ons_df, xwOBA)

  return xBA


# %%
n_df = statcast_batting_stats(regular_season)
n_df.loc[n_df["AB"] > 100].sort_values("xSLG", ascending=False).head(10)

# %%
add_ons.loc[add_ons["is_sac_fly"], ["estimated_woba_using_speedangle"]]
# add_ons["events"].value_counts()

# %%
add_ons["launch_speed"]