#%%
import pandas as pd, numpy as np
import statcast_dataset as sd, get_player as gp, add_on as ao

pd.set_option('display.max_columns', 500)

idlookup_df = pd.read_csv('data/IDLookupTable.csv')

# loading 2025 season from statcast
# sav25 = sd.loadSav('2025-2-20','2025-06-25',idlookup_df )
# sav25.to_csv('data/sav25.csv')

sav25 = pd.read_csv('data/sav25.csv')

# print(sav25.head())

# print(sav25[['game_date','player_name','pitch_name','release_speed']].head())

df = ao.add_ons(sav25,idlookup_df)


# %%
df.head()
# %%
df['game_date'].unique()
# %%
df['game_date'].sort_values(ascending=False)
# %%
