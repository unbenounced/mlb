import pandas as pd, numpy as np
from unidecode import unidecode


pa_flag_dict = {'field_out':1,'nan':0,'strikeout':1,'double':1,'strikeout_double_play':1,
                'single':1,'force_out':1,'hit_by_pitch':1,'grounded_into_double_play':1,
                'home_run':1,'walk':1,'caught_stealing_2b':0,'sac_bunt':1,'triple':1,
                'sac_fly':1,'field_error':1,'double_play':1,'catcher_interf':1,'fielders_choice_out':1,
                'fielders_choice':1,'pickoff_1b':0,'other_out':0,'caught_stealing_home':0,'pickoff_caught_stealing_2b':0,
                'caught_stealing_3b':0,'sac_fly_double_play':1,'pickoff_caught_stealing_home':0,'pickoff_2b':0,'run':0,
                'triple_play':1,'batter_interference':1,'pickoff_3b':0,'sac_bunt_double_play':1,'pickoff_caught_stealing_3b':0}

ab_flag_dict = {'field_out':1,'nan':0,'strikeout':1,'double':1,
                'strikeout_double_play':1,'single':1,'force_out':1,'hit_by_pitch':0,
                'grounded_into_double_play':1,'home_run':1,'walk':0,'caught_stealing_2b':0,
                'sac_bunt':0,'triple':1,'sac_fly':0,'field_error':1,
                'double_play':1,'catcher_interf':0,'fielders_choice_out':1,'fielders_choice':1,
                'pickoff_1b':0,'other_out':0,'caught_stealing_home':0,'pickoff_caught_stealing_2b':0,
                'caught_stealing_3b':0,'sac_fly_double_play':1,'pickoff_caught_stealing_home':0,'pickoff_2b':0,
                'run':0,'triple_play':1,'batter_interference':1,'pickoff_3b':0,'sac_bunt_double_play':1,'pickoff_caught_stealing_3b':0}

is_hit_dict = {'field_out':0,'nan':0,'strikeout':0,'double':1,'strikeout_double_play':0,
                'single':1,'force_out':0,'hit_by_pitch':0,'grounded_into_double_play':0,'home_run':1,
                'walk':0,'caught_stealing_2b':0,'sac_bunt':0,'triple':1,'sac_fly':0,
                'field_error':0,'double_play':0,'catcher_interf':0,'fielders_choice_out':0,'fielders_choice':0,
                'pickoff_1,b':0,'other_out':0,'caught_stealing_home':0,'pickoff_caught_stealing_2b':0,'caught_stealing_3b':0,
                'sac_fly_double_play':0,'pickoff_caught_stealing_home':0,'pickoff_2b':0,'run':0,'triple_play':0,'batter_interference':0,
                'pickoff_3b':0,'sac_bunt_double_play':0,'pickoff_caught_stealing_3b':0}

is_hit_list = ['single','double','triple','homerun']

swing_dict = {'ball':0,'foul_tip':1,'called_strike':0,'swinging_strike':1, 'pitchout': 0, 'bunt_foul_tip': 1,
                'foul':1,'hit_into_play_no_out':1,'hit_into_play':1,'hit_into_play_score':1, 'missed_bunt': 1,
                'hit_by_pitch':0,'blocked_ball':0,'swinging_strike_blocked':1, 'foul_bunt': 1}

fair_contact_dict = {'ball':0,'foul_tip':0,'called_strike':0,'swinging_strike':0, 'pitchout': 0,
                'foul':0,'hit_into_play_no_out':1,'hit_into_play':1, 'missed_bunt': 0,
                'hit_into_play_score':1,'hit_by_pitch':0, 'bunt_foul_tip': 0,
                'blocked_ball':0,'swinging_strike_blocked':0, 'foul_bunt': 0}

foul_contact_dict = {'ball':0,'foul_tip':0,'called_strike':0,'swinging_strike':0, 'pitchout': 0,
                'foul':1,'hit_into_play_no_out':1,'hit_into_play':1, 'missed_bunt': 0,
                'hit_into_play_score':1,'hit_by_pitch':0, 'bunt_foul_tip': 0,
                'blocked_ball':0,'swinging_strike_blocked':0, 'foul_bunt': 1}

inplay_dict = {'ball':0,'foul_tip':0,'called_strike':0,'swinging_strike':0, 'pitchout': 0, 'bunt_foul_tip': 0,
              'foul':0,'hit_into_play_no_out':1,'hit_into_play':1,'hit_into_play_score':1,  'missed_bunt': 0,
              'hit_by_pitch':0,'blocked_ball':0,'swinging_strike_blocked':0, 'foul_bunt': 0}

isoutdict = {'field_out':1, 'strikeout':1,'grounded_into_double_play':2,
             'sac_bunt':1,'fielders_choice_out':1, 'fielders_choice':0,
             'force_out':1,'caught_stealing_3b':1,'caught_stealing_2b':1, 'double_play':2,
             'strikeout_double_play':2,'sac_fly_double_play':2, 'sac_fly':1,
             'other_out':1,'pickoff_caught_stealing_3b':1,'triple_play':3,
             'pickoff_1b':1,'sac_bunt_double_play':2,'caught_stealing_home':1,
             'pickoff_2b':1,'pickoff_3b':1}

my_des_dict = {'ball': 'Ball', 'hit_into_play': 'In Play', 'called_strike': 'Called Strike',
          'foul': 'Foul', 'swinging_strike': 'Whiff', 'blocked_ball': 'Ball',
          'swinging_strike_blocked': 'Whiff', 'foul_tip': 'Foul', 'foul_bunt': 'Foul',
          'missed_bunt': 'whiff', 'pitchout': 'Ball', 'bunt_foul_tip': 'Foul'}

def add_ons(sav,idlookup_df):
  p_lookup_dict = gp.id_dic(idlookup_df)

  sav['game_date'] = pd.to_datetime(sav['game_date'])
  sav = sav.sort_values(by='game_date')
  sav['the_pa_id'] = sav['game_pk'].astype(str) + sav['at_bat_number'].astype(str)
  sav['pitch_id'] = sav['game_pk'].astype(str) + sav['pitcher'].astype(str) + sav['batter'].astype(str) + sav['at_bat_number'].astype(str) + sav['pitch_number'].astype(str)
  sav['game_month'] = pd.DatetimeIndex(sav['game_date']).month
  sav['PitchesThrown'] = 1

  sav['BatterName'] = sav['batter'].map(p_lookup_dict)
  nanbatters = list(sav[sav['BatterName'].isna()]['batter'].unique())

  print('Getting missing batter ids - {} players'.format(len(nanbatters)))
  gp.getPlayerName_list(nanbatters,idlookup_df)

  print('Got them all, re-mapping')
  p_lookup_dict = gp.id_dic(idlookup_df)

  sav['BatterName'] = sav['batter'].map(p_lookup_dict)
  sav['BatterName'] = sav['BatterName'].apply(unidecode)

  sav['player_name'] = sav['player_name'].str.split(', ').str[::-1].str.join(' ')
  sav['player_name'] = sav['player_name'].apply(unidecode)
  sav['pitch_name'] = sav['pitch_name'].replace({'2-Seam Fastball': 'Sinker', 'Knuckle Curve': 'Curveball', 'Fastball': '4-Seam Fastball'})
  sav['pitch_type'] = sav['pitch_type'].replace({'KC': 'CU', 'FA': 'FF'})

  sav['IsHomeSP'] = np.where((sav['inning']==1)&(sav['balls']==0)&(sav['strikes']==0)&(sav['inning_topbot']=='Top')&(sav['outs_when_up']==0)&(sav['away_score']==0)&(sav['on_1b'].isna())&(sav['on_2b'].isna())&(sav['on_3b'].isna()),1,0)
  sav['IsRoadSP'] = np.where((sav['inning']==1)&(sav['balls']==0)&(sav['strikes']==0)&(sav['inning_topbot']=='Bot')&(sav['outs_when_up']==0)&(sav['home_score']==0)&(sav['on_1b'].isna())&(sav['on_2b'].isna())&(sav['on_3b'].isna()),1,0)

  sav['PA_flag'] = sav['events'].map(pa_flag_dict)
  sav['PA_flag'] = sav['PA_flag'].fillna(0)

  sav['AB_flag'] = sav['events'].map(ab_flag_dict)
  sav['AB_flag'] = sav['AB_flag'].fillna(0)

  sav['Is_Hit'] = sav['events'].isin(is_hit_list).astype(int)
 
  sav['SwungOn'] = sav['description'].map(swing_dict)
  sav['ContactMade_Fair'] = sav['description'].map(fair_contact_dict)
  sav['ContactMade_Foul'] = sav['description'].map(foul_contact_dict)
  sav['BallInPlay'] = sav['description'].map(inplay_dict)
  sav['IsFoul'] = np.where(sav['description'].isin(['foul']),1,0)

  sav['IsShift'] = np.where((sav['if_fielding_alignment']=='Infield shift')&(sav['PA_flag']==1),1,0)

  sav['OutsMade'] = sav['events'].map(isoutdict)

  sav['IsSwStr'] = np.where(sav['description'].isin(['swinging_strike','swinging_strike_blocked','missed_bunt','foul_tip']),1,0)
  sav['IsCalledStr'] = np.where(sav['description']=='called_strike',1,0)
  sav['IsWhiff'] = np.where((sav['IsSwStr']==1)&(sav['SwungOn']==1),1,0)
  sav['IsStrike'] = np.where(sav['type']=='S',1,0)
  sav['IsBall'] = np.where(sav['type']=='B',1,0)

  sav['zone'] = sav['zone'].fillna(0)
  sav['InZone'] = np.where(sav['zone']<10,1,0)
  sav['OutZone'] = np.where(sav['zone']>9,1,0)
  sav['InZoneFlag'] = np.where(sav['zone']<10,'Y','N')
  sav['IsChase'] = np.where(((sav['SwungOn']==1)&(sav['InZone']==0)),1,0)
  sav['IsZoneSwing'] = np.where(((sav['SwungOn']==1)&(sav['InZone']==1)),1,0)
  sav['IsZoneContact'] = np.where(((sav['ContactMade_Foul']==1)&(sav['InZone']==1)),1,0)

  sav['IsSingle'] = np.where(sav['events']=='single',1,0)
  sav['IsDouble'] = np.where(sav['events']=='double',1,0)
  sav['IsTriple'] = np.where(sav['events']=='triple',1,0)
  sav['IsHomer'] = np.where(sav['events']=='home_run',1,0)
  sav['IsStrikeout'] = np.where(sav['events'].isin(['strikeout','strikeout_double_play']),1,0)
  sav['IsWalk'] = np.where(sav['events']=='walk',1,0)
  sav['IsHBP'] = np.where(sav['events']=='hit_by_pitch',1,0)
  sav['IsXBH'] = np.where((sav['IsDouble']==1)|(sav['IsTriple']==1)|(sav['IsHomer']==1),1,0)

  sav['IsBIP'] = np.where(sav['type']=='X',1,0)
  sav['IsGB'] = np.where(sav['bb_type']=='ground_ball',1,0)
  sav['IsLD'] = np.where(sav['bb_type']=='line_drive',1,0)
  sav['IsFB'] = np.where(sav['bb_type']=='fly_ball',1,0)
  sav['IsPU'] = np.where(sav['bb_type']=='popup',1,0)

  sav['launch_speed_angle'] = sav['launch_speed_angle'].fillna(0)
  sav['IsBrl'] = np.where(sav['launch_speed_angle']==6,1,0)
  sav['IsSolid'] = np.where(sav['launch_speed_angle']==5,1,0)
  sav['IsWeak'] = np.where((sav['launch_speed_angle']>0)&(sav['launch_speed_angle']<4),1,0)

  sav['launch_speed_bip'] = np.where(sav['type']=='X',sav['launch_speed'],np.nan)
  sav['launch_angle_bip'] = np.where(sav['type']=='X',sav['launch_angle'],np.nan)
  sav['launch_speed'] = sav['launch_speed'].fillna(0)
  sav['launch_angle'] = sav['launch_angle'].fillna(0)

  sav['IsBunt'] = np.where((sav['IsBIP']==1)&((sav['des'].str.contains('Bunt'))|(sav['des'].str.contains('bunt'))),1,0)

  sav['estimated_ba_using_speedangle'] = np.where((sav['AB_flag']==1)&(sav['estimated_ba_using_speedangle'].isna()),0,sav['estimated_ba_using_speedangle'])
  sav['estimated_woba_using_speedangle'] = np.where((sav['AB_flag']==1)&(sav['estimated_woba_using_speedangle'].isna()),0,sav['estimated_woba_using_speedangle'])
  sav['estimated_woba_using_speedangle'] = np.where(sav['IsWalk']==1,.7,sav['estimated_woba_using_speedangle'])

  sav['BlastCrit1'] = np.where(((sav['launch_speed'].isna())|(sav['launch_speed']<100)|(sav['type']!='X')),(0),(1))
  sav['BlastCrit2'] = np.where(((sav['launch_angle']<=28)&((28-sav['launch_angle'])<=((sav['launch_speed']-100)))),(1),(0))
  sav['BlastCrit3'] = np.where((sav['launch_angle']>28)&((sav['launch_angle']-28)<=((sav['launch_speed']-100)*3)),(1),(0))
  sav['IsBlast'] = np.where((sav['BlastCrit1']!=0)&((sav['BlastCrit2']+sav['BlastCrit3']>0)),1,0)

  sav['IsHardHit'] = np.where(((sav['launch_speed']>=95)&(sav['type']=='X')),1,0)

  sav['IsBrlHomer'] = np.where((sav['IsBrl']==1)&(sav['IsHomer']==1),1,0)
  sav['IsBlastHomer'] = np.where((sav['IsBlast']==1)&(sav['IsHomer']==1),1,0)
  sav['IsHardHit_Hit'] = np.where((sav['IsHardHit']==1)&(sav['Is_Hit']==1),1,0)

  sav['GS'] = np.where((sav['inning']==1)&(sav['bat_score']==0)&(sav['balls']==0)&(sav['outs_when_up']==0)&(sav['strikes']==0)&(sav['pitch_number']==1)&(sav['on_1b'].isna())&(sav['on_2b'].isna())&(sav['on_3b'].isna()),1,0)

  sav['Month'] = sav['game_date'].dt.month
  monthnamedict = {3:'March',4:'April',5:'May',6:'June',7:'July',8:'August',9:'September',10:'October'}
  sav['Month'] = sav['Month'].replace(monthnamedict)

  pitch_categories = {'4-Seam Fastball': 'Fastball', 'Changeup': 'Offspeed', 'Slider': 'Breaking',
                    'Curveball': 'Breaking', 'Sinker': 'Fastball', 'Cutter': 'Fastball',
                    'Split-Finger': 'Offspeed', 'Knuckle Curve': 'Breaking', 'Fastball': 'Fastball',
                    'Screwball': 'Breaking','Eephus': 'Offspeed','Knuckleball': 'Offspeed',
                    'Sweeper': 'Breaking', 'Slow Curve': 'Breaking', 'Slurve': 'Breaking', 'Forkball': 'Offspeed'}

  sav['PitchGroup'] = sav['pitch_name'].map(pitch_categories)

  sav['BatterTeam'] = np.where(sav['inning_topbot']=='Top', sav['away_team'], sav['home_team'])
  sav['PitcherTeam'] = np.where(sav['inning_topbot']=='Top', sav['home_team'], sav['away_team'])

  sav = sav.drop_duplicates(subset=['game_pk','at_bat_number','pitch_number'])

  return(sav)