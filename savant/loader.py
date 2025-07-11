from __future__ import annotations

import os
import random
import time
from pathlib import Path
from typing import List

import pandas as pd 
import pybaseball as pyb 
import requests
from bs4 import BeautifulSoup, Comment
from unidecode import unidecode

# ──────────────────────── Paths ────────────────────────
DATA_DIR = Path("savant/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ──────────────────────── Helpers ────────────────────────
def id_dic(idlookup_df: pd.DataFrame) -> dict[int, str]:
  """Turn ID‑lookup DataFrame into {MLBID: PLAYERNAME} dict."""
  clean = idlookup_df.loc[:, ~idlookup_df.columns.str.contains('^Unnamed')]
  return dict(zip(clean["MLBID"], clean["PLAYERNAME"]))

def data_file_update(df: pd.DataFrame, filename: str) -> None:
  (DATA_DIR / f"{filename}.csv").write_text(df.to_csv(index=False))

def read_data_file(filename: str) -> pd.DataFrame:
  return pd.read_csv(DATA_DIR / f"{filename}.csv")

# ────────────────── Statcast ETL ──────────────────
def load_sav(
  startdate: str = "",
  enddate: str = "",
) -> pd.DataFrame:
  return pyb.statcast(startdate, enddate)

 # ────────────────── Player‑name back‑fill ──────────────────
USER_AGENT_LIST = [
  # Windows Desktop
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.170 Safari/537.36",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:116.0) Gecko/20100101 Firefox/116.0",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edg/116.0.1938.81",
  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) OPR/100.0.0.0 Chrome/115.0.5790.170 Safari/537.36",

  # macOS Desktop
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.170 Safari/537.36",
  "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5; rv:116.0) Gecko/20100101 Firefox/116.0",

  # Android Mobile
  "Mozilla/5.0 (Linux; Android 14; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.170 Mobile Safari/537.36",
  "Mozilla/5.0 (Linux; Android 14; SM-G998U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/22.0 Chrome/115.0.5790.170 Mobile Safari/537.36",
  "Mozilla/5.0 (Linux; Android 14; rv:116.0) Gecko/116.0 Firefox/116.0 Mobile",
  "Mozilla/5.0 (Linux; Android 14; U; en-US; SM-G991U Build/RP1A.200720.012) AppleWebKit/537.36 (KHTML, like Gecko) UCBrowser/14.1.20.1008 Mobile Safari/537.36",
  "Mozilla/5.0 (Linux; Android 14; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.5790.170 Mobile Safari/537.36 YaBrowser/23.3.0.273 YaApp_Android/11.91 YaFeature/YaVoiceAssistant",

  # iOS Mobile / Tablet
  "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
  "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/115.0.5790.98 Mobile/15E148 Safari/604.1",

  # Amazon Silk (Fire Tablet)
  "Mozilla/5.0 (Linux; Linux armv7l; KFFOWI) AppleWebKit/537.36 (KHTML, like Gecko) Silk/110.4.3 like Chrome/110.0.5481.100 Safari/537.36",
] 

def idlookup_new(
  idlookup_df: pd.DataFrame,
  nan_batters: List[int],
  session: requests.Session | None = None,
) -> pd.DataFrame:
  """Fetch missing player names from MLB API and return updated DF."""
  if session is None:
    session = requests.Session()

  rows: list[dict[str, str | int]] = []
  for pid in nan_batters:
    url = f"https://statsapi.mlb.com/api/v1/people/{pid}"
    time.sleep(random.uniform(0.5,2.0))
    session.headers.update({'User-Agent': random.choice(USER_AGENT_LIST)})

    try:
      people = session.get(url, timeout=7).json().get("people", [])
      if people:
        rows.append(
            {"MLBID": pid,"PLAYERNAME": people[0].get("fullName", "")}
        )
      else:
        print(f"No data for {pid}")
    except (requests.RequestException, ValueError) as exc:
      print(f"Request failed for {pid}: {exc}")

  if rows:
    new = pd.DataFrame(rows)
    return pd.concat([idlookup_df, new], ignore_index=True)
  
  return idlookup_df

def find_nanbatters(
  sav: pd.DataFrame,
  idlookup_df: pd.DataFrame
) -> pd.DataFrame:
  """
  Checks for missing batter IDs in idlookup_df and fetches names via MLB API if needed.
  Returns an updated idlookup_df.
  """
  # Finding id's that are NOT in the lookup
  missing_ids = list(set(sav["batter"]) - set(id_dic(idlookup_df)))  
  if missing_ids:
    idlookup_df = idlookup_new(idlookup_df, missing_ids)
  
  return idlookup_df
  
# ────────────────── Main ──────────────────
def main() -> None:
  today = pd.Timestamp.today().normalize()
  yesterday = today - pd.Timedelta(days=1)
  
  try:
    sav25 = read_data_file("sav25")
    sav25["game_date"] = pd.to_datetime(sav25["game_date"])

    latest_in_file = sav25["game_date"].max().floor("D")
    if latest_in_file < yesterday:
      missing = load_sav(
        latest_in_file.strftime("%Y-%m-%d"),
        yesterday.strftime("%Y-%m-%d"),
      )
      sav25 = pd.concat([sav25, missing], ignore_index=True)
  except FileNotFoundError:
    sav25 = load_sav("2025-02-20", yesterday.strftime("%Y-%m-%d"))

  idlookup_df = read_data_file("IDLookupTable")
  idlookup_df = find_nanbatters(sav25, idlookup_df)

  data_file_update(sav25,"sav25")
  print("sav25 updated →", DATA_DIR / "sav25.csv")

if __name__ == "__main__":
  main()