import pandas as pd, os, requests, warnings
from unidecode import unidecode
from bs4 import BeautifulSoup, Comment

def dropUnnamed(df):
    df = df.loc[:,~df.columns.str.contains('^Unnamed')]
    return(df)

def id_dic():
    idlookup_df = pd.read_csv('IDLookupTable.csv')
    idlookup_df = dropUnnamed(idlookup_df)

    return dict(zip(idlookup_df.MLBID,idlookup_df.PLAYERNAME))

def getPlayerName_list(pidlist):
    for playerid in pidlist:
        try:
          url = 'https://statsapi.mlb.com/api/v1/people/{}'.format(str(playerid))

          pagejson = requests.get(url).json()
          playername = pagejson.get('people')[0].get('fullname')
          print('Found name {} for ID {}'.format(playername,playerid))
          new_idlookup_df = pd.DataFrame({'MLBID':playerid,'PLAYERNAME':playername},ignore_index=True)
          idlookup_df = pd.concat([idlookup_df,new_idlookup_df])

        except:
          print('Found nothing for {}'.format(playerid))
          pass
    
    idlookup_df = dropUnnamed(idlookup_df)
    idlookup_df.to_csv('IDLookupTable.csv')