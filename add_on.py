import pandas as pd, numpy as np, unidecode
import get_player as gp

def add_ons(sav):
    id_lookup_df = gp.id_dic()
    sav['game_date'] = pd.to_datetime(sav['game_date'])