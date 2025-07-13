from __future__ import annotations
import pandas as pd
import pandas as np
from unidecode import unidecode
import config as cfg

# unique pitch identifier
sav25["pitch_id"] =  (
  sav25["game_pk"].astype(str) 
  + sav25["pitcher"].astype(str) 
  + sav25["batter"].astype(str) 
  + sav25["at_bat_number"].astype(str) 
  + sav25["pitch_number"].astype(str)
)
sav25 = sav25.drop_duplicates(subset="pitch_id")

sav["pitcher_name"] = (
  sav["player_name"].str.split(", ").str[::-1].str.join(" ")
)

sav["player_name"] = sav["player_name"].apply(unidecode)
  # ►  Trans‑literate to plain ASCII  ◄
sav["batter_name"] = sav["batter_name"].apply(unidecode)