#%%
from __future__ import annotations

from pathlib import Path

import pandas as pd
import numpy as np
import config as cfg
from unidecode import unidecode

# ──────────────────────── Paths ────────────────────────
DATA_DIR = Path("data")
if not DATA_DIR.exists():
  DATA_DIR = Path("savant/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

lookup = pd.read_csv(DATA_DIR / "IDLookupTable.csv")
sav = pd.read_csv(DATA_DIR / "sav25.csv")

# ──────────────────────── Helpers ────────────────────────
# %%
def normalize_names(sav: pd.DataFrame, lookup: pd.DataFrame) -> pd.DataFrame:
  out = sav.copy()
  out["batter_name"] = out["batter"].map(dict(zip(lookup["MLBID"], lookup["PLAYERNAME"])))
  out["batter_name"] = out["batter_name"].apply(unidecode)

  out["pitcher_name"] = out["player_name"].str.split(', ').str[::-1].str.join(' ')
  out["pitcher_name"] = out["pitcher_name"].apply(unidecode)

  return out
# %%
def add_pitch_ids(sav: pd.DataFrame) -> pd.DataFrame:
  out = sav.copy()
  out["pitch_id"] =  (
    out["game_pk"].astype(str) 
    + out["pitcher"].astype(str) 
    + out["batter"].astype(str) 
    + out["at_bat_number"].astype(str) 
    + out["pitch_number"].astype(str)
  )
  out['pa_id'] = (out["game_pk"].astype(str) + out["at_bat_number"].astype(str))
  return out.drop_duplicates(subset="pitch_id")

# %%
def prepare_game_dates(sav: pd.DataFrame) -> pd.DataFrame:
  out = sav.copy()
  """Convert game_date to datetime, sort by date, and extract game month."""
  out["game_date"] = pd.to_datetime(out["game_date"])
  out["game_month"] = out["game_date"].dt.month
  out["month"] = out["game_date"].dt.month
  out["month"] = out["month"].replace(cfg.month_name_dict)
  out = out.sort_values(by="game_date", ascending=False)
  return out

def pitches(sav: pd.DataFrame) -> pd.DataFrame:
  out = sav.copy()
  out["pitches_thrown"] = 1
  out["pitch_name"] = out["pitcher_name"].replace(cfg.pitch_name_dict)
  out["pitch_type"] = out["pitch_type"].replace(cfg.pitch_type_dict)
  return out

# %%
def pitcher_flags(sav: pd.DataFrame) -> pd.DataFrame:
  out = sav.copy()
  out.loc[
    (out["inning"]==1)
    &(out ["balls"]==0)
    &(out ["strikes"]==0)
    &(out ["inning_topbot"]=="Top")
    &(out ["outs_when_up"]==0)
    &(out["away_score"]==0)
    &(out ["on_1b"].isna())
    &(out ["on_2b"].isna())
    &(out ["on_3b"].isna()),
    "home_sp"
  ] = 1
  out["home_sp"] = out["home_sp"].fillna(0).astype(int)
  out.loc[
    (out["inning"]==1) &
    (out ["balls"]==0) &
    (out ["strikes"]==0) &
    (out ["inning_topbot"]=="Bot") &
    (out ["outs_when_up"]==0) &
    (out["home_score"]==0) &
    (out ["on_1b"].isna()) &
    (out ["on_2b"].isna()) &
    (out["on_3b"].isna()),
    "away_sp"
  ] = 1
  out["away_sp"] = out["away_sp"].fillna(0).astype(int)
  return out


# %%
def batter_stats(sav: pd.DataFrame) -> pd.DataFrame:
  out = sav.copy()
  out["plate_appearance"] = out["events"].isin(cfg.pa_flag_list).astype(int)
  out["at_bat"] = out["events"].isin(cfg.ab_flag_list).astype(int)
  out["hit"] = out["events"].isin(cfg.is_hit_list).astype(int)
  out["swing"] = out["description"].isin(cfg.swing_list).astype(int)
  out["fair_ball"] = out["description"].isin(cfg.fair_contact_list).astype(int)
  out["foul_ball"] = out["description"].isin(cfg.foul_contact_list).astype(int)
  out["in_play"] = out["description"].isin(cfg.inplay_list).astype(int)
  out["foul"] = out["description"].isin(cfg.foul_list).astype(int)
  out["outs_made"] = out["events"].map(cfg.is_out_dict)
  return out

# %%
def defense(sav: pd.DataFrame) -> pd.DataFrame:
  out = sav.copy()
  out["shift_on"] = ((out["if_fielding_alignment"].isin(cfg.infield_alignment_list)) & (out["plate_appearance"] == 1)).astype(int)
  return out


# %%
def pitcher_stats(sav: pd.DataFrame) -> pd.DataFrame:
  out = sav.copy()
  out["swinging_strike"] = out["description"].isin(cfg.swinging_strike_list).astype(int)
  out["called_strike"] = out["desctipion"].isin(cfg.called_strike_list).astype(int)
  out["whiff"] = ((out["swinging_strike"] == 1) & (out["swing"] == 1)).astype(int)
  return out
# %%
def add_ons(sav: pd.DataFrame, lookup: pd.DataFrame) -> pd.DataFrame:
  sav = normalize_names(sav, lookup)
  sav = add_pitch_ids(sav)
  sav = prepare_game_dates(sav)
  sav = pitches(sav)
  sav = pitcher_flags(sav)
  sav = pitcher_stats(sav)
  sav = batter_stats(sav)
  sav = defense(sav)
  return sav

# %%
pd.set_option('display.max_columns', 500)
# %%
new_sav = add_ons(sav, lookup)
new_sav.head()
# %%
print(new_sav["at_bat"].isna().sum())
# %%
new_sav["shift_on"].value_counts()
# %%
new_sav["if_fielding_alignment"].value_counts()
# %%
sav = add_ons(sav, lookup)
sav.head()
# %%
sav["shift_on"].value_counts()
# %%
