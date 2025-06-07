import pandas as pd, pybaseball as pyb
import get_player as gp

def loadSav(startdate,enddate):
  # format = YYYY-MM-DD
  sav = pyb.statcast(start_dt=startdate,end_dt=enddate)
  sav['BatterName'] = sav['batter'].map(gp.id_dic())
  sav['player_name'] = sav['pitcher'].map(gp.id_dic())
  return(sav)

def yesterday_sav():
  sav = pyb.statcast()
  sav['BatterName'] = sav['batter'].map(gp.id_dic())
  sav['player_name'] = sav['pitcher'].map(gp.id_dic())
  return(sav)

