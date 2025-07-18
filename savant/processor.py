#%%
from __future__ import annotations

from pathlib import Path

import pandas as pd
import pandas as np
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
pd.set_option('display.max_columns', 500)
sav.head()
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
def add_ons(sav, lookup):
  sav = normalize_names(sav, lookup)
  sav = add_pitch_ids(sav)
  sav = prepare_game_dates(sav)
  sav = pitches(sav)
  return sav
# %%
new_sav = add_ons(sav, lookup)
new_sav.head()

# %%
