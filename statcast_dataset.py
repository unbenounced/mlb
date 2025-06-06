import pybaseball as pyb
import pandas as pd
import get_player as gp



def loadSav(startdate,enddate):
    sav = pyb.statcast(start_dt=startdate,end_dt=enddate)
    sav['BatterName'] = sav['batter'].map(gp.id_dic())
    sav['player_name'] = sav['pitcer'].map(gp.id_dic())
    return(sav)
