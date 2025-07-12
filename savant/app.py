#%%
import pandas as pd, numpy as np

pd.set_option('display.max_columns', 500)
# %%
sav25 = pd.read_csv('data/sav25.csv')
# %%
sav25 = sav25.sort_values('game_date',ascending=False)

# %%
sav25['pitch_type'].isna().sum()
# %%
sav25['pitch_type'].notna().sum()  
# %%
sav25.loc[sav25['pitch_type'].isna()]
# %%
sav25['game_date'].head()
# %%
sav25['batter_name'].isna().sum()
# %%
