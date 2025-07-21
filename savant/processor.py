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
def normalize_names(sav: pd.DataFrame, lookup: pd.DataFrame) -> pd.DataFrame:
  out = sav.copy()

  out["batter_name"] = out["batter"].map(dict(zip(lookup["MLBID"], lookup["PLAYERNAME"])))
  out["batter_name"] = out["batter_name"].apply(unidecode)

  out["pitcher_name"] = out["player_name"].str.split(', ').str[::-1].str.join(' ')
  out["pitcher_name"] = out["pitcher_name"].apply(unidecode)

  return out

def add_pitch_ids(sav: pd.DataFrame) -> pd.DataFrame:
  out = sav.copy()

  out = out.drop_duplicates(subset=["game_pk", "at_bat_number", "pitch_number"])

  out["pitch_id"] =  (
    out["game_pk"].astype(str) 
    + out["pitcher"].astype(str) 
    + out["batter"].astype(str) 
    + out["at_bat_number"].astype(str) 
    + out["pitch_number"].astype(str)
  )
  out['pa_id'] = (out["game_pk"].astype(str) + out["at_bat_number"].astype(str))

  return out

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

def pitcher_flags(sav: pd.DataFrame) -> pd.DataFrame:
  out = sav.copy()

  out["is_home_sp"] = (
    (out["inning"]==1) &
    (out ["balls"]==0) &
    (out ["strikes"]==0) &
    (out ["inning_topbot"]=="Top") &
    (out ["outs_when_up"]==0) &
    (out["away_score"]==0) &
    (out ["on_1b"].isna()) &
    (out ["on_2b"].isna()) &
    (out ["on_3b"].isna())
  )
 
  out["is_away_sp"] = (
    (out["inning"]==1) &
    (out["balls"]==0) &
    (out["strikes"]==0) &
    (out["inning_topbot"]=="Bot") &
    (out["outs_when_up"]==0) &
    (out["home_score"]==0) &
    (out["on_1b"].isna()) &
    (out["on_2b"].isna()) &
    (out["on_3b"].isna())
  )

  out["is_game_starter"] = (
    (out["inning"]==1) &
    (out["bat_score"]==0) &
    (out["balls"]==0) &
    (out["outs_when_up"]==0) &
    (out["strikes"]==0) &
    (out["pitch_number"]==1) &
    (out["on_1b"].isna()) &
    (out["on_2b"].isna()) &
    (out["on_3b"].isna())
  )

  return out

def batter_stats(sav: pd.DataFrame) -> pd.DataFrame:
  out = sav.copy()

  out["is_plate_appearance"] = out["events"].isin(cfg.pa_flag_list)
  out["is_atbat"] = out["events"].isin(cfg.ab_flag_list)
  out["is_hit"] = out["events"].isin(cfg.is_hit_list)
  out["is_swing"] = out["description"].isin(cfg.swing_list)
  out["is_fair_ball"] = out["description"].isin(cfg.fair_contact_list)
  out["is_foul_ball"] = out["description"].isin(cfg.foul_contact_list)
  out["is_in_play"] = out["description"].isin(cfg.inplay_list)
  out["is_foul"] = out["description"].isin(cfg.foul_list)
  out["is_outs_made"] = out["events"].map(cfg.is_out_dict)

  out["is_single"] = out["events"].isin(cfg.single_list)
  out["is_double"] = out["events"].isin(cfg.double_list)
  out["is_triple"] = out["events"].isin(cfg.triple_list)
  out["is_homerun"] = out["events"].isin(cfg.homerun_list)
  out["is_strikeout"] = out["events"].isin(cfg.strikeout_list)
  out["is_walk"] = out["events"].isin(cfg.walk_list)
  out["is_hit_by_pitch"] = out["events"].isin(cfg.hit_by_pitch)
  out["is_extra_base_hit"] = (out["is_double"] | out["is_triple"] | out["is_homerun"])

  out["is_ball_in_play"] = out["type"].isin(cfg.ball_in_play_list)
  out["is_groundball"] = out["bb_type"].isin(cfg.groundball_list)
  out["is_linedrive"] = out["bb_type"].isin(cfg.linedrive_list)
  out["is_flyball"] = out["bb_type"].isin(cfg.flyball_list)
  out["is_popup"] = out["bb_type"].isin(cfg.popup_list)

  out["launch_speed_angle"] = out["launch_speed_angle"].fillna(0)
  out["is_barrel"] = out["launch_speed_angle"] == 6
  out["is_solid"] = out["launch_speed_angle"] == 5
  out["is_weak"] = (out["launch_speed_angle"] > 0) & (out["launch_speed_angle"] < 4)

  out["launch_speed_bip"] = np.where(out["is_ball_in_play"], out["launch_speed"], np.nan)
  out["launch_angle_bip"] = np.where(out["is_ball_in_play"], out["launch_angle"], np.nan)
  
  # sav["launch_speed"] = sav["launch_speed"].fillna(0) - use when needed
  # sav["launch_angle"] = sav["launch_angle"].fillna(0) - use when needed

  out["is_bunt"] = ((out["is_ball_in_play"]) & (out["des"].str.contains("bunt", case=False, na=False)))

  out.loc[(out["is_atbat"]) & (out["estimated_ba_using_speedangle"].isna()), "estimated_ba_using_speedangle"] = 0
  out.loc[(out["is_atbat"]) & (out["estimated_woba_using_speedangle"].isna()), "estimated_woba_using_speedangle"] = 0

  out.loc[out["is_walk"], "estimated_woba_using_speedangle"] = .7

  # Need to explore
  out["blast_criteria_1"] = ((out["launch_speed"] >= 100) & out["is_ball_in_play"])
  out["blast_criteria_2"] = (out["launch_angle"] <= 28) & ((28 - out["launch_angle"]) <= (out["launch_speed"] - 100))
  out["blast_criteria_3"] = (out["launch_angle"] > 28) & ((out["launch_angle"] - 28) <= ((out["launch_speed"] - 100) * 3))
  out["is_blast"] = out["blast_criteria_1"] & out["blast_criteria_2"] | out["blast_criteria_3"]

  out["is_hardhit"] = (out["launch_speed"] >= 95) & out["is_atbat"]

  out["is_barrel_homerun"] = out["is_barrel"] & out["is_homerun"]
  out["is_blast_homerun"] = out["is_blast"] & out["is_homerun"]
  out["is_hardhit_hit"] = out["is_hardhit"] & out["is_hit"]

  return out

def defense(sav: pd.DataFrame) -> pd.DataFrame:
  out = sav.copy()

  out["shift_on"] = ((out["if_fielding_alignment"].isin(cfg.infield_alignment_list)) & (out["is_plate_appearance"]))

  return out

def pitcher_stats(sav: pd.DataFrame) -> pd.DataFrame:
  out = sav.copy()

  out["is_swinging_strike"] = out["description"].isin(cfg.swinging_strike_list)
  out["is_called_strike"] = out["description"].isin(cfg.called_strike_list)
  out["is_whiff"] = (out["is_swinging_strike"] & out["is_swing"])
  out["is_strike"] = out["type"].isin(cfg.strike_list)
  out["is_ball"] = out["type"].isin(cfg.ball_list)

  out["zone"] = out["zone"].fillna(0)

  out["in_zone"] = out["zone"].between(1, 9)
  out["out_of_zone"] = ~out["in_zone"]

  out["is_chase"] = (out["is_swing"] & out["in_zone"])
  out["in_zone_swing"] = (out["is_swing"] & out["in_zone"])
  out["in_zone_foul"] = (out["is_foul_ball"] & out["in_zone"])

  return out

def add_ons(sav: pd.DataFrame, lookup: pd.DataFrame) -> pd.DataFrame:
  sav = normalize_names(sav, lookup)
  sav = add_pitch_ids(sav)
  sav = prepare_game_dates(sav)
  sav = pitches(sav)
  sav = pitcher_flags(sav)
  sav = batter_stats(sav)
  sav = pitcher_stats(sav)
  sav = defense(sav)

  return sav

pd.set_option('display.max_columns', 500)

new_sav = add_ons(sav, lookup)
new_sav.head()
