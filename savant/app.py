#%%
import pandas as pd, numpy as np

pd.set_option('display.max_columns', 500)
# %%
sav25 = pd.read_csv('data/sav25.csv')
# %%
sav25.sort_values('game_date',ascending=False).head()
# %%
sav25['pitch_id'] =  sav25['pitcher'].astype(str) + sav25['batter'].astype(str) + sav25['at_bat_number'].astype(str) + sav25['pitch_number'].astype(str)
# %%
sav25.head()
# %%
sav25['game_date'].dt.strftime('%Y%m%d').head()

# %%
