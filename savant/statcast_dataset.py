import pandas as pd, pybaseball as pyb
import get_player as gp

def loadSav(startdate,enddate,idlookup_df):
  # format = YYYY-MM-DD
  sav = pyb.statcast(start_dt=startdate,end_dt=enddate)
  sav['BatterName'] = sav['batter'].map(gp.id_dic(idlookup_df))
  sav['player_name'] = sav['pitcher'].map(gp.id_dic(idlookup_df))
  return(sav)

def yesterday_sav(idlookup_df ):
  sav = pyb.statcast()
  sav['BatterName'] = sav['batter'].map(gp.id_dic(idlookup_df))
  sav['player_name'] = sav['pitcher'].map(gp.id_dic(idlookup_df))
  return(sav)

