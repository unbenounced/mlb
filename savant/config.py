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

pa_flag_list = [
  "field_out", "strikeout", "double", "strikeout_double_play", "single", "force_out", "hit_by_pitch", 
  "grounded_into_double_play", "home_run", "walk", "sac_bunt", "triple", "sac_fly", "field_error", "double_play", 
  "catcher_interf", "fielders_choice_out", "fielders_choice", "sac_fly_double_play", "triple_play",
  "batter_interference", "sac_bunt_double_play"
]


ab_flag_list = [
  "field_out", "strikeout", "double", "strikeout_double_play", "single", "force_out", "grounded_into_double_play",
  "home_run", "triple", "field_error", "double_play", "fielders_choice_out", "fielders_choice", "sac_fly_double_play",
  "triple_play", "batter_interference", "sac_bunt_double_play"
]

is_hit_list = ["single", "double", "triple", "homerun"]

swing_list = [
  "foul_tip", "swinging_strike", "bunt_foul_tip", "foul", "hit_into_play_no_out", "hit_into_play",
  "hit_into_play_score", "missed_bunt", "swinging_strike_blocked", "foul_bunt"
]

fair_contact_list = ["hit_into_play_no_out", "hit_into_play", "hit_into_play_score"]

foul_contact_list = ["foul", "hit_into_play_no_out", "hit_into_play", "hit_into_play_score", "foul_bunt"]

inplay_list = ["hit_into_play_no_out", "hit_into_play", "hit_into_play_score"]

is_out_dict = {
  "fielders_choice": 0, "field_out": 1, "strikeout": 1, "sac_bunt": 1, "fielders_choice_out": 1, "force_out": 1, "caught_stealing_3b": 1, 
  "caught_stealing_2b":1, "sac_fly": 1, "other_out": 1, "pickoff_caught_stealing_3b":1, "pickoff_1b": 1, "caught_stealing_home": 1, 
  "pickoff_2b": 1, "pickoff_3b": 1, "sac_bunt_double_play": 2,  "strikeout_double_play": 2, "sac_fly_double_play": 2, "double_play": 2, 
  "grounded_into_double_play": 2,"triple_play": 3
}

my_des_dict = {
  "ball": "Ball", "hit_into_play": "In Play", "called_strike": "Called Strike",
  "foul": "Foul", "swinging_strike": "Whiff", "blocked_ball": "Ball",
  "swinging_strike_blocked": "Whiff", "foul_tip": "Foul", "foul_bunt": "Foul",
  "missed_bunt": "whiff", "pitchout": "Ball", "bunt_foul_tip": "Foul"
}

month_name_dict = {3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October"}

pitch_name_dict = {"2-Seam Fastball": "Sinker", "Knuckle Curve": "Curveball", "Fastball": "4-Seam Fastball"}

pitch_type_dict = {"KC": "CU", "FA": "FF"}
