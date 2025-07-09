import pandas as pd, pybaseball as pyb, os, requests, warnings, time, random
from unidecode import unidecode
from bs4 import BeautifulSoup, Comment

# turns id look up dataframe into a dictionary
def id_dic(idlookup_df):
  idlookup_df = idlookup_df.loc[:, ~idlookup_df.columns.str.contains('^Unnamed')]
  return dict(zip(idlookup_df.MLBID,idlookup_df.PLAYERNAME))

def data_file_update(df,filename):
  path = f'savant/data/{filename}.csv'
  df.to_csv(path,index=False)

def read_data_file(filename):
  path = f'savant/data/{filename}.csv'
  return pd.read_csv(path) 

# get missing players from their player id numbers from the mlb api
def idlookup_new(idlookup_df,nan_batters):
  session = requests.Session()

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

  rows = []

  for playerid in nan_batters:
    url = f'https://statsapi.mlb.com/api/v1/people/{playerid}'

    time.sleep(random.uniform(0.5,2.0)) # wait between 0.5 and 2 seconds

    session.headers.update({
      'User-Agent': random.choice(USER_AGENT_LIST)
    })

    try:
      resp = session.get(url)
      resp.raise_for_status() # throws for 4xx/5xx
      people = resp.json().get('people', [])
      if not people:
        print(f"No data for {playerid}")
        continue

      fullname = people[0].get('fullName')
      rows.append({'MLBID':playerid,'PLAYERNAME':fullname})

    except requests.RequestException as e:
      # network error or bad HTTP status
      print(f"Request failed for {playerid}:{e}")
    except (KeyError, IndexError, TypeError) as e:
      #JSON structure wasn't what we expected
      print(f"JSON parsing failed for {playerid}:{e}")

  new_idlookup_df = pd.DataFrame(rows)
  idlookup_df = pd.concat([idlookup_df, new_idlookup_df], ignore_index=True)


def getPlayerName_list(pidlist,idlookup_df):
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

  data_file_update(idlookup_df,'IDLookupTable')


def load_sav(idlookup_df,startdate="",enddate=""):
  # format = YYYY-MM-DD
  sav = pyb.statcast(startdate,enddate)
  id_lookup = id_dic(idlookup_df)

  sav['batter_name'] = sav['batter'].map(id_lookup)
  sav['pitcher_name'] = sav['player_name'].str.split(', ').str[::-1].str.join(' ')

  # get batters names who are not in the idlookup_df
  nan_mask = sav['batter_name'].isna()

  nan_batters = sav.loc[nan_mask, 'batter'].unique().tolist()
  print(len(nan_batters))
  
  if len(nan_batters) > 0: 
    idlookup_df = idlookup_new(idlookup_df,nan_batters)
    sav.loc[nan_mask, 'batter_name'] = sav.loc[nan_mask, 'batter'].map(id_lookup)
  
  return(sav)


today = pd.to_datetime('today')
idlookup_df = read_data_file('IDLookupTable')
yesterday = today - pd.Timedelta('1 day')
try:
  sav25 = read_data_file('sav25')
  sav25['game_date'] = pd.to_datetime(sav25['game_date'])

  if pd.to_datetime(sav25['game_date'].max()) != pd.to_datetime(yesterday.floor('D')):
    missing_days_df = load_sav(idlookup_df,sav25['game_date'].max().strftime('%Y-%m-%d'),yesterday.strftime('%Y-%m-%d'))
    sav25 = pd.concat([sav25,missing_days_df],ignore_index=True)

    # wire up removing dulicates
    #sav25['pitch_id'] = sav25['']

    # save updated file to drive
    data_file_update(sav25,'sav25')

except FileNotFoundError:
  sav25 = load_sav(idlookup_df,'2025-02-20',yesterday.strftime('%Y-%m-%d'))
  data_file_update(sav25,'sav25')

