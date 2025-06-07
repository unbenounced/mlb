import pandas as pd, numpy as np
import statcast_dataset as sd, get_player as gp, add_on as ao

df = pd.read_csv('data/sav_data.csv')
idlookup_df = pd.read_csv('data/IDLookupTable.csv')

nwe = ao.add_ons(df,idlookup_df)

print(nwe.head())