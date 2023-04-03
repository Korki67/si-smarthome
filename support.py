# -*- coding: utf-8 -*-

DASH_OBJ = {
  "speak":	{ "speak": "", "time": -1, "error": 0 },
  "xml":	{ "speak": "", "time": -1, "error": 0 }
}

SPEAK_OBJ = { "time": -1, "dev": "none", "text": "none" }

BLOCK_OBJ = { "until": -1, "time": -1, "by": "9.0.99" }

ALARM_OBJ = {
  "type"        : "none",
  "level"       : 20,
  "prio"        :  4,
  "rank"        : 28,
  "reason"      : "none",
  "action"      : "none",
  "time"        : -1,
  "device"      : "none",
  "trigger"     : '9/0/99'
}

EVENT_OBJ = {
  "type"        : "none",
  "group"	: "9/0/99",
  "time"        : -1,
  "speak"       : copy.deepcopy(SPEAK_OBJ),
  'alarm'	: copy.deepcopy(ALARM_OBJ),
  'block'	: copy.deepcopy(BLOCK_OBJ),
  "act"		: -1,
  "flag"	: "n/a",
  "num"		: -1,
  "minV"	: -1,
  "maxV"	: -1,
  "minE"	: "9/0/99",
  "maxE"	: "9/0/99"
}

ELEM_OBJ = {
  "type"        : "none",
  "flag"	: "n/a",
  "time"	: -1,
  "act"		: -1,
  "min"		: -1,
  "max"		: -1,
  "alter"	: -1,
  "source"	: -1,
  "last_time"	: -1,
  "last_act"	: -1,
  "last_alter"	: -1,
  "last_source"	: -1,
  "message"	: "",
  "alarm"   	: copy.deepcopy(ALARM_OBJ),
  "speak"   	: copy.deepcopy(SPEAK_OBJ),
  "block" 	: copy.deepcopy(BLOCK_OBJ)
}

ROOM_OBJ = {
  'name'	: "",
  'light_mode'	: {"act": -1, "time": -1},
  'blind_mode'	: {"act": -1, "time": -1},
  'time'	: -1,
  'speak'	: copy.deepcopy(SPEAK_OBJ),
  'alarm'	: copy.deepcopy(ALARM_OBJ)
}

FLAT_OBJ = {
  'name'	: "CB194",
  'speak'       : copy.deepcopy(SPEAK_OBJ),
  'speed'	: { 'time': 0, 'PING': 0, 'UPLO': 0, 'DOWN': 0 },
  'persons'	: { 'act': '-', 'time': -1 },
  'beauf'	: { "speed_av": -1, "speed_mx": -1, "beauf_av": -1, "beauf_mx": -1, "time": -1 }
}

Garage = {
  1	: { "act": -1, "pre": -1, "time": 0.0 },
  2	: { "act": -1, "pre": -1, "time": 0.0 },
  3	: { "act": -1, "pre": -1, "time": 0.0 }
}

dh_norm    = 0  
dh_Niesel  = 1  
dh_Regen   = 2  
dh_heavy   = 3  

ds_na      = -1 
ds_none    = 0  
ds_little  = 1  
ds_moder   = 2  
ds_full    = 3  

wetter_codes    = {
#code     Text                                      Icon   Dh
200: ["Gewitter mit leichtem Regen"      , " 11d", dh_Niesel, ds_none  ],
201: ["Gewitter mit Regen"               , " 11d", dh_Regen , ds_none  ],
202: ["Gewitter mit starkem Regen"       , " 11d", dh_heavy , ds_none  ],
210: ["leichtes Gewitter"                , " 11d", dh_Niesel, ds_none  ],
211: ["Gewitter"                         , " 11d", dh_norm  , ds_none  ],
212: ["starkes Gewitter"                 , " 11d", dh_norm  , ds_none  ],
221: ["extremes Gewitter"                , " 11d", dh_norm  , ds_none  ],
230: ["Gewitter mit leichtem Niesel"     , " 11d", dh_Niesel, ds_none  ],
231: ["Gewitter mit Niesel"              , " 11d", dh_Niesel, ds_none  ],
232: ["Gewitter mit starkem Niesel"      , " 11d", dh_Niesel, ds_none  ],
300: ["leichter Niesel"                  , " 09d", dh_Regen , ds_none  ],
301: ["Niesel"                           , " 09d", dh_Regen , ds_none  ],
302: ["sehr intensiver Niesel"           , " 09d", dh_Regen , ds_none  ],
310: ["leichter Nieselregen"             , " 09d", dh_Niesel, ds_none  ],
311: ["Nieselregen"                      , " 09d", dh_Niesel, ds_none  ],
312: ["sehr intensiver Nieselregen"      , " 09d", dh_Niesel, ds_none  ],
313: ["Regenschauer und Niesel"          , " 09d", dh_Niesel, ds_none  ],
314: ["starke Regenschauer und Niesel"   , " 09d", dh_Regen , ds_none  ],
321: ["Nieselregen und Schauer"          , " 09d", dh_Niesel, ds_none  ],
500: ["leichter Regen"                   , " 10d", dh_Regen , ds_none  ],
501: ["moderater Regen"                  , " 10d", dh_Regen , ds_none  ],
502: ["sehr intensiver Regen"            , " 10d", dh_heavy , ds_none  ],
503: ["sehr starker Regen"               , " 10d", dh_heavy , ds_none  ],
504: ["extremer Regen"                   , " 10d", dh_heavy , ds_none  ],
511: ["frierender Regen"                 , " 13d", dh_Regen , ds_none  ],
520: ["leichter Regenschauer"            , " 09d", dh_Regen , ds_none  ],
521: ["Regenschauer"                     , " 09d", dh_Regen , ds_none  ],
522: ["sehr intensiver Regenschauer"     , " 09d", dh_Regen , ds_none  ],
531: ["extreme Regenschauer"             , " 09d", dh_Regen , ds_none  ],
600: ["leichter Schnee"                  , " 13d", dh_Regen , ds_none  ],
601: ["Schnee"                           , " 13d", dh_Regen , ds_none  ],
602: ["starker Schnee"                   , " 13d", dh_Regen , ds_none  ],
611: ["Schneeregen"                      , " 13d", dh_Regen , ds_none  ],
612: ["Schneeregenschauer"               , " 13d", dh_Regen , ds_none  ],
615: ["leichter Regen und Schnee"        , " 13d", dh_Regen , ds_none  ],
616: ["Regen und Schnee"                 , " 13d", dh_Regen , ds_none  ],
620: ["leichte Schneeschauer"            , " 13d", dh_Niesel, ds_none  ],
621: ["Schneeschauer"                    , " 13d", dh_Niesel, ds_none  ],
622: ["starke Schneeschauer"             , " 13d", dh_Niesel, ds_none  ],
701: ["Neben"                            , " 50d", dh_norm  , ds_na    ],
711: ["Rauch"                            , " 50d", dh_norm  , ds_na    ],
721: ["Dunst"                            , " 50d", dh_norm  , ds_na    ],
731: ["Sand und Staubwirbel"             , " 50d", dh_norm  , ds_na    ],
741: ["Nebel"                            , " 50d", dh_norm  , ds_na    ],
751: ["Sand"                             , " 50d", dh_norm  , ds_na    ],
761: ["Staub"                            , " 50d", dh_norm  , ds_na    ],
762: ["vulkanische Asche"                , " 50d", dh_norm  , ds_na    ],
771: ["Böen"                             , " 50d", dh_norm  , ds_na    ],
781: ["Tornado"                          , " 50d", dh_norm  , ds_na    ],
800: ["klarer Himmel"                    , " 01d", dh_norm  , ds_full  ],
801: ["leicht bewölkt"                   , " 02d", dh_norm  , ds_full  ],
802: ["aufgelockerte Bewölkung"          , " 03d", dh_norm  , ds_moder ],
803: ["aufgelockerte Bewölkung"          , " 04d", dh_norm  , ds_moder ],
804: ["bewölkt"                          , " 04d", dh_norm  , ds_moder ]
}

#########################
#       RUN TIMER	#
#########################
# TIMER['4/3/5'] = { 'time': knx_time+30, 'value': 0, 'cond_group': "4/3/5", 'cond_value': 2 }
def run_timer():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, knx_time
  global TIMER

  V = conf_data['Verbosity']['timer']

  DEL = []
  for T in TIMER:
    if knx_time > TIMER[T]['time']:
      try:    flag = ELEM_DATA[TIMER[T]['cond_group']]['act'] == TIMER[T]['cond_value']
      except: flag = False
      verbose_print(V,f"Group {T} setting to {TIMER[T]['value']} aborted {flag}")
      if not flag: knx_write(T, TIMER[T]['value'])
      DEL.append(T)

  for D in DEL: del TIMER[D]

#########################
#     VERBOSE_PRINT     #
#########################
def verbose_print(level, message):
  global conf_data, mess_file

  if conf_data["General"]["verbosity"] >= level:
    print((datetime.now().strftime("%Y.%m.%d %H:%M:%S: ") + message))
    if conf_data["General"]["verlogity"] >= level:
      f = open(mess_file, 'a')
      f.write(datetime.now().strftime("%Y.%m.%d %H:%M:%S: ") + message + '\n')
      f.close()

#########################
#     READ_CONFIG       #
#########################
def load_conf():
  global conf_data, conf_file, software_config_time
  global MOBILE

  if software_config_time == os.path.getmtime(conf_file): return False

  conf_data = {}
  f = open(conf_file, 'r', encoding='iso-8859-1')
  group = "General"
  conf_data[group] = {}
  param_old = ""
  for line in f:
    try:
      code = line.split('#')[0].strip()
      (param, value) = code.split('=', 1)
    except:
      param = ""
      value = ""

    if True:
      param = param.strip()
      value = value.strip()
      if (param == "") and (value != ""):
        param = param_old

      if (param != "") or (value != ""):
        try:
          param = float(param)
          if param == int(param): param = int(param)
        except: pass
        try:
          value = float(value)
          if value == int(value): value = int(value)
        except: pass
        if param == param_old:
          if conf_data[group][param] is not None and not isinstance(conf_data[group][param], list):
            conf_data[group][param] = [conf_data[group][param]]
          conf_data[group][param].append(value)
        else:
          conf_data[group][param] = value

        if group == "Orte1":
          LOC = {param : [int(x) for x in value.split(',')] }
          MOBILE['LOC'][1].update(LOC)
        if group == "Orte2":
          LOC = {param : [int(x) for x in value.split(',')] }
          MOBILE['LOC'][2].update(LOC)
      if (param != "") and (value != ""):
        param_old = param

    if min(line.find('['), line.find(']')) >= 0:
      group = line[line.find('[')+1:line.find(']')]
      if group != "General": conf_data[group] = {}
  f.close()

  if conf_data["General"]["version"] != software_version:
    info_system_log("halt", "config invalid", "")
    quit
    
  if (software_config_time < -0.5):
    info_system_log("start", "program started", "")
    verbose_print(conf_data['Verbosity']['load_conf'],"config file read.")
  else:
    info_system_log("info" , "config change", "")
    verbose_print(conf_data['Verbosity']['load_conf'],"updated config file read.")

  software_config_time = os.path.getmtime(conf_file)

  FLAT_OBJ['persons']['act']  = "-" * len(conf_data['Persons'])
  FLAT_OBJ['persons']['time'] = time.time()

  update_elem_conf()
  extract_lights_conf()

  return True

######################################
# start, stop, config & log messages #
######################################
def info_system_log(hint, mess, info):
  global software_name
  if software_name == "temp": return

  try:    os.system('/home/pi/info-system/info-log ' + software_name + ' ' + hint + ' "' + mess + '" ' + info)
  except: pass

def info_system_mail(hint, subj, file):
  global software_name
  try:    os.system('/home/pi/info-system/info-mail ' + software_name + ' ' + hint + ' "' + subj + '" ' + file)
  except: pass

def goodbye():
  global software_name
  if software_name == "temp": return
  try:    info_system_log("stop", "program ended", "") 
  except: pass

atexit.register(goodbye)

def recover_knx():
  global knx_bus

  knx_bus_error = knx_bus.poll()
  info_system_mail('ALARM', "KNX bus failure. Trying to recover ...", 'mail_knx-error.txt')
  verbose_print(1,"KNX bus failure error {:s}".format(str(knx_bus_error)))

  i = 0
  while knx_bus_error is not None:
    time.sleep(5.0)
    knx_bus = subprocess.Popen(['groupsocketlisten', 'ip:192.168.22.65'], \
              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1.0)
    verbose_print(1,"KNX recovery loop #{:02d}".format(i))
    knx_bus_error = knx_bus.poll()
    i += 1 

  info_system_mail('OK', "KNX bus recovered.", '/home/pi/eHome/knx_recovered.txt')
  verbose_print(1,"KNX bus recovered. Continuing ...".format(str(knx_bus_error)))

#########################
#     SAVE & LOAD VARS	#
#########################
def save_vars():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, vars_file, min1_last
  global LIGHTS, BLINDS, MOBILE

  # avoid saving just after loading at start
  if min1_last == -1: return

  f = open(vars_file + '.tmp', 'wb')
  pickle.dump(ELEM_DATA, f)
  pickle.dump(ROOM_DATA, f)
  pickle.dump(FLAT_DATA, f)
  pickle.dump(LIGHTS, f)
  pickle.dump(Garage, f)
  pickle.dump(DASH_DATA, f)
  pickle.dump(MOBILE, f)
  pickle.dump(BLINDS, f)
  f.close()
  os.system('mv ' + vars_file + '.tmp ' + vars_file)
  verbose_print(conf_data['Verbosity']['save_vars'],"Variables saved.")

def load_vars():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, vars_file
  global LIGHTS, BLINDS, MOBILE

  if os.path.exists(vars_file):
    f = open(vars_file, 'rb')
    try:
      i = 0
      ELEM_DATA	 = pickle.load(f)
      i = 1
      ROOM_DATA	 = pickle.load(f)
      i = 2
      FLAT_DATA	 = pickle.load(f)
      i = 3
      LIGHTS	 = pickle.load(f)
      i = 4
      Garage	 = pickle.load(f)
      i = 5
      DASH_DATA	 = pickle.load(f)
      i = 6
      MOBILE	 = pickle.load(f)
      i = 7
      BLINDS	 = pickle.load(f)
      i = 8
      verbose_print(1,"Variables fully loaded.")
    except:
      verbose_print(1,f"Variables {i:d}/8 elements loaded.")
    f.close()
  else:
    verbose_print(1,"File with variables does not exist. Starting empty.")

#########################
#  UPDATE ELEMENTS CONF #
#########################
def update_elem_conf():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, min1_last, vars_file

  V = 1 if os.path.exists(vars_file) else 5

  # scan all elements in current data to be deleted
  del_list = []
  for E in ELEM_DATA:
    try:    config = conf_data["Elements"][E]
    except: del_list.append(E)

  for E in del_list:
    verbose_print(V, "ELEMENT DEL " + E)
    del ELEM_DATA[E]

  # scan all elements in config to be added or updated
  for E in conf_data["Elements"]:
    try:
      config = str(ELEM_DATA[E]['act'])
    except:
      if min1_last != -1: verbose_print(1,'ELEMENT ADD '+E)
      ELEM_DATA[E] = copy.deepcopy(ELEM_OBJ)
      config = "ADD"

    # set or update master data
    dat = conf_data["Elements"][E].split(';')
    ELEM_DATA[E]["ID"]		= dat[0].strip()
    ELEM_DATA[E]["name"]	= dat[1].strip()
    ELEM_DATA[E]["type"]	= dat[2].strip()
    ELEM_DATA[E]["room"]	= int(dat[3])
    ELEM_DATA[E]["visu"]	= dat[4].strip()
    ELEM_DATA[E]["symbol"]	= dat[5].strip() + "," + dat[6].strip()

  # create FLAT if not exist
  try: FLAT_DATA
  except:
    FLAT_DATA = copy.deepcopy(FLAT_OBJ)

  # create all rooms by scanning the elements
  for E in conf_data["Elements"]:

    # create and / or update ROOM_DATA
    Room = ELEM_DATA[E]["room"]
    if not (conf_data['General']['room_no_min'] <= Room <= conf_data['General']['room_no_max']):
      raise Exception(f"Room {Room:d} out of range " + \
                      f"{conf_data['General']['room_no_min']:d}-{conf_data['General']['room_no_max']:d}")

    try: ROOM_DATA[Room]
    except:
      ROOM_DATA[Room] = copy.deepcopy(ROOM_OBJ)
      name, device = conf_data['Rooms'][Room].split(',')
      ROOM_DATA[Room]['name']         = name.strip()
      ROOM_DATA[Room]['speak']['dev'] = device.strip()
      if software_config_time != -1: verbose_print(V,f"New room {Room:2d} created.")

  # create all types of events in all rooms, dash and in flat by scanning the elements
  for E in conf_data["Elements"]:
    Type = ELEM_DATA[E]["type"]

    try:    DASH_DATA[Type]
    except:
      DASH_DATA[Type] = copy.deepcopy(DASH_OBJ)

    for i in ROOM_DATA:
      try: ROOM_DATA[i][Type]
      except:
        ROOM_DATA[i][Type] = copy.deepcopy(EVENT_OBJ)
        if software_config_time != -1: verbose_print(V,f"New room {i:2d} type {Type:<10s} created.")

    try: FLAT_DATA[Type]
    except:
      FLAT_DATA[Type] = copy.deepcopy(EVENT_OBJ)
      if software_config_time != -1: verbose_print(V,f"New type {Type:<10s} in FLAT created.")

#########################
#   UPDATE LIGHT MODES  #
#########################
def extract_lights_conf():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, conf_data, LIGHTS

  LIGHTS = [dict() for x in range(9)]
  for C in conf_data["LightModes"]:
    mode = int(C.split('-')[0])
    eiba =    (C.split('-')[1])
    D = [x.strip() for x in conf_data["LightModes"][C].split(',')]
    LIGHTS[mode][eiba] = [D[0], int(D[1]), int(D[2]), int(D[3]), int(D[4])]

#########################
#     WEATHER		#
#########################
def load_weather():
  global WEATHER, DASH_DATA

  # URL oeffnen und XML Daten einlesen
  # &u=c am Ende fuer Wetter in Grad Celsius
  try:
    f = open('weather.xml', 'r')
    tree = f.read()
    tree = '<response>\n' + tree + '</response>\n'
    f.close()
  except:
    verbose_print(2, "Error 1 - could not read weather file")
    return

  # xml Daten parsen und in Baumstruktur anordnen
  old_weather = copy.deepcopy(WEATHER)
  try:
    temp = xmltodict.parse(tree)
    WEATHER = temp['response']
    temp = float(WEATHER['w_T_outside'])
  except:
    verbose_print(1, "Error 2 - could not decode weather file")
    verbose_print(1, "Error 2 - restoring previous weather data")
    WEATHER = copy.deepcopy(old_weather)
    return

  try:    DASH_DATA['wetter']
  except: DASH_DATA['wetter'] = copy.deepcopy(DASH_OBJ)
  dash_mode = "xml"
  dash_wetter("detail")
  V = conf_data["General"]["verbose_weather"]
  verbose_print(V,"weather successfully read")
  ROOM_DATA[11]["temp"]["act"] = float(WEATHER['w_T_outside'])
  ROOM_DATA[12]["temp"]["act"] = float(WEATHER['w_T_outside'])
  ROOM_DATA[13]["temp"]["act"] = float(WEATHER['w_T_outside'])
  ROOM_DATA[11]["humi"]["act"] = float(WEATHER['w_humi_0'])
  ROOM_DATA[12]["humi"]["act"] = float(WEATHER['w_humi_0'])
  ROOM_DATA[13]["humi"]["act"] = float(WEATHER['w_humi_0'])

  ROOM_DATA[11]["temp"]["time"] = time.time()
  ROOM_DATA[12]["temp"]["time"] = time.time()
  ROOM_DATA[13]["temp"]["time"] = time.time()
  ROOM_DATA[11]["humi"]["time"] = time.time()
  ROOM_DATA[12]["humi"]["time"] = time.time()
  ROOM_DATA[13]["humi"]["time"] = time.time()
  WEATHER['sun_height'], WEATHER['sun_azimuth'] = sun_position(datetime.now())
  verbose_print(V,"Sun height {:.1f} / angle {:.1f}".format(WEATHER['sun_height'], WEATHER['sun_azimuth']))

  sun_rise = float(WEATHER['w_sunrise'])
  sun_set  = float(WEATHER['w_sunset'])
  sun_act  = int(0.5 + 100. *(time.time() - sun_rise) / (sun_set - sun_rise))
  SUN_RISE = datetime.fromtimestamp(int(WEATHER['w_sunrise']))
  SUN_SET  = datetime.fromtimestamp(int(WEATHER['w_sunset']))
  verbose_print(V,"Sun_rise " + SUN_RISE.strftime("%H:%M:%S") + " sun_set " + SUN_SET.strftime("%H:%M:%S"))
  verbose_print(V,"Sun {:.1f}%".format(sun_act))
  code = WEATHER["w_num"]
  verbose_print(V,"Weather num {:s} code {:d}".format(code, wetter_codes[int(code)][3]))

#########################
#     SUN_POSITION      #
#########################
def sun_position(sun_time):

  # source: www.geoastro.de/SME/tk/index.htm
  
  # COLOGNE
  lat		= 50.93603
  long		=  6.91159
  
  # correct daylight saving time (DST)
  if time.localtime().tm_isdst:
    sun_time += DT.timedelta(hours=-1)

  # actual time
  tageszahl	= sun_time.timetuple().tm_yday
  monat		= sun_time.timetuple().tm_mon
  datum		= sun_time.timetuple().tm_mday
  stunde	= sun_time.timetuple().tm_hour
  minute	= sun_time.timetuple().tm_min
  
  # calculation
  K		=  0.01745
  deklin		= -23.45*math.cos(K*360.*(tageszahl+10.)/365.)
  zeitgleichung	= 60.*(-0.171*math.sin(0.0337*tageszahl+0.465)-0.1299*math.sin(0.01787*tageszahl-0.168))
  stundenwinkel	= 15.*(stunde+minute/60.-(15.0-long)/15.0-12.+zeitgleichung/60.)
  x		= math.sin(K*lat)*math.sin(K*deklin)+math.cos(K*lat)*math.cos(K*deklin)*math.cos(K*stundenwinkel)
  hoehe		= math.asin(x)/K
  y		= -(math.sin(K*lat)*math.sin(K*hoehe)-math.sin(K*deklin))/(math.cos(K*lat)*math.sin(math.acos(math.sin(K*hoehe))))
  if stunde+minute/60. <= 12+(15-long)/15-zeitgleichung/60:
    azimut	= math.acos(y)/K
  else:
    azimut	= 360. - math.acos(y)/K
    
  # if hoehe < 0.0: azimut = 359.0

  return (hoehe, azimut)

#########################
#   LET ALEXA SPEAK     #
#########################
def smart_speaker(dev, spe, lou, rad, room, weight):
  global ELEM_DATA, ROOM_DATA, conf_data

  # ----------------------------------------------------
  # prio   = 0 .. 10 for item having issue
  # level  = 0 ..  2 for level of issue
  # weight = prio + 2 x level
  # ----------------------------------------------------
  #  0 ..  5 > desaster      > always
  #  6 .. 12 > important     > only during media-hours
  # 13 .. 16 > nice to have  > only during media-hours
  # ----------------------------------------------------

  if not (0 <= room < 10):
    verbose_print(1, f"invalid room from {dev} {spe} room {room}.")
    info_system_mail('ALARM', f"invalid room from {dev} {spe} room {room}.", 'mail_knx-error.txt')
    return

  if (rad != "-") or (spe != "#"):
    MediaOK = check_time('4/3/'+str(room), 'sound') or (weight <= 5)
    verbose_print(1,"alexa dev {:s} radio {:s} speak {:s} => MediaOK {:d} weight {:d}".format(dev, rad, spe[0:35], MediaOK, weight))
    if not MediaOK:
      rad = "-"
      spe = "-"

  if (rad == "-") and (ROOM_DATA[room]["light_mode"]["act"] > 0):
    rad = "cont"

  if rad != "-":
    ROOM_DATA[room]['speak']['time']   = time.time()
    ROOM_DATA[room]['speak']['radio']  = rad
    try:
      if lou != "AUTO": ROOM_DATA[room]['speak']['loud'] = lou
    except: pass

  if dev == "-": dev = "Sued1"
  if dev == "alle":
    if ELEM_DATA['4/3/6']['act'] == 3: dev = "alle-6"
    hour = time.localtime()[3]
    if (hour < 8) or (hour > 22): dev = "info-6"

  comm = "./alexa {:s} '{:s}' {:d} '{:s}'".format(dev, spe, lou, rad)
  os.system('sudo -u www-data screen -S queue -X stuff "' + comm + ' >> /var/www/ehome-cgi-bin/alexa.log 2>&1 ^M"')
  
def knx_write(w_group, w_value):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, conf_data
  global LIGHTS, BLINDS

  V = conf_data['Verbosity']['knx']

  os.system(f"./knx_write {w_group:s} {w_value:d} > /dev/null &")
  verbose_print(V,f"writing knx {w_group:s} value {w_value:d}")

#########################
#	CHECK TIME      #
#########################
def check_time(group, media):
  global ELEM_DATA, ROOM_DATA, conf_data
  global WEATHER

  # group => room, 
  # media => media_wday/wend

  if media == "n/a": return False

  # INITIATE THE DAY
  # ===================
  now = datetime.now()
  act  = now.hour*60+now.minute
  room = ELEM_DATA[group]["room"]
  offset = (now.hour > 12)
  wday = now.weekday()			# weekday() 0=Monday
  tag = datetime.now() + DT.timedelta(days=offset)
  tag = tag.strftime("%Y-%m-%d")

  # READ CONFIG TIMES
  # ===================
  try:
    if ((wday + offset) in [5, 6]): # or (tag in HOLIDAYS):
      try:    OKtime = conf_data["Room"+str(room)][media+'_wend']
      except: OKtime = conf_data["General"][media+'_wend']
    else:
      try:    OKtime = conf_data["Room"+str(room)][media+'_wday']
      except: OKtime = conf_data["General"][media+'_wday']
  except:
     verbose_print(1,"media {:s} not found in room {:d}".format(media, room))
     OKtime = media
  
  spec = OKtime.split(',')

  MediaResult = False
  if OKtime == "n/a": return False

  for zeit in spec:
    if zeit in ["daytime", "nighttime"]:
      SUN_RISE = datetime.fromtimestamp(int(WEATHER['w_sunrise']))
      SUN_SET  = datetime.fromtimestamp(int(WEATHER['w_sunset']))
      t1 = SUN_RISE.hour*60+SUN_RISE.minute
      t2 = SUN_SET.hour *60+SUN_SET.minute
      if OKtime == "daytime": tx = "-"
      else                  : tx = "x"
    
    else:
      tx = zeit[5:6]
      if not (tx in ['-', 'x']): tx = '#'
      try:
        if tx == '-': t1, t2 = zeit.split('-')
        else        : t1, t2 = zeit.split('x')
      except:
        verbose_print(1,"Error for {:s} media {:s} in check_time {:s} of {:s} separator {:s}".format(group, media, zeit, OKtime, tx))
        return False
  
      h,m  = t1.split(':')
      t1 = int(h)*60+int(m)
      h,m  = t2.split(':')
      t2   = int(h)*60+int(m)
    
    if (t1 < t2):
      MediaOK = (t1 <= act < t2)
      if tx == 'x': MediaOK = not MediaOK
    else:
      MediaOK = (act <= t2) or (t1 < act)
      if tx == 'x': MediaOK = not MediaOK
  
    MediaResult = MediaResult or MediaOK

  return MediaResult

#########################
#	RUN MACROS      #
#########################
def run_macro(group, value, source):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, conf_data
  global LIGHTS, BLINDS

  V = conf_data['Verbosity']['macros']
  verbose_print(V,f"group {group:s} value {value:d} source {source:s}")

  if not isinstance(conf_data['Macros'][group], list):
    conf_data['Macros'][group] = [conf_data['Macros'][group]]
  for M in conf_data['Macros'][group]:
    media, typus, content, logic = M.split('~')
    if   logic == "1": value = max(value,0)
    elif logic == "2": value = 1 - min(1, max(value,0))
    elif logic == "3": value = 3 * max(value,0)
    elif logic == "4": value = 4 * max(value,0)
    elif logic == "5": value = 1
    elif logic == "0": value = 0
    elif logic == "10": value = max(value,0)
    elif logic == "11": value = max(value,0)
    else:
      raise Exception("Error 1 in Macro " + group + " " + M)

    # special case: fan
    if (group == '0/3/19') and (value == 2):
      value = ELEM_DATA['0/3/19']['act']

    if value != 0:
      MediaOK = check_time(group, media)

      # Sonder-Regel fuer Gaeste WC / Bad2
      Zeit = ELEM_DATA['0/0/17']['time']
      delta_gang = conf_data["Room9"]["delta_gang"]
      act = ELEM_DATA['0/0/17']['act']
      if (act == 0) and (not MediaOK) and (typus == "eib") and (content == "0/0/19") and \
         ((time.time() - Zeit > delta_gang) or (FLAT_DATA["persons"]['act'].find('V') == -1)):
        MediaOK = True
    else:
      MediaOK = True

    if (logic == "0") and (value == 0):
      MediaOK = True
    if (logic == "0") and (value >  0):
      MediaOK = False
    #if (logic == "3") and (value <  1):
    #  MediaOK = False
    if (logic == "5") and (value <  1): # ???
      MediaOK = False

    if MediaOK:
      if   typus == "TV":
        for R in BLINDS:
          if (ELEM_DATA[R]["room"] == int(content)) and (BLINDS[R][0][-1] == "a"):
            if (media == "TVday") or ((value == 0) and (ELEM_DATA[group]["last_act"] == 1)):
              os.system('groupswrite ip:192.168.22.65 ' + R + ' ' + str(value) + ' > /dev/null')
            BLINDS[R][1] = time.time() + conf_data["Blinds"]["movie_time"] * 60.0*60. * float(value*2-1)

      elif typus == "man":
        if source == "hardware":
          os.system('groupswrite ip:192.168.22.65 ' + content + ' ' + str(value) + ' > /dev/null &')
          verbose_print(V, 'groupswrite ip:192.168.22.65 ' + content + ' ' + str(value) + ' > /dev/null &')
    
      elif typus == "eib":
        os.system('groupswrite ip:192.168.22.65 ' + content + ' ' + str(value) + ' > /dev/null &')
        verbose_print(V, 'groupswrite ip:192.168.22.65 ' + content + ' ' + str(value) + ' > /dev/null &')
    
      elif typus == "url":
        if len(logic) == 1:
          if value < 0.0: raise Exception(f"value {value:f} < 0 in marco for URL from {group:s}")
          if int(value) != value: raise Exception(f"non-int value {value:f} in marco for URL from {group:s}")

          os.system('wget -q --delete-after http://' + content.replace('&','\&') + str(value)+' &')
          verbose_print(V, 'urllib.urlopen(http://' + content + str(value)+').read()')
        else:
          if ((logic == "10") and (value == 0)) or ((logic == "11") and (value == 1)):
            os.system('wget -q --delete-after http://' + content.replace('&','\&')             +' &')
            verbose_print(V, "wget: " + content)
    
      elif typus == "water":
        verbose_print(conf_data["Alarm"]["water_verbose"],group+" Wasser "+str(ELEM_DATA[group]["act"]))
        if ELEM_DATA[group]["act"] == 0:
          dash_all("details")
          touch_room(ELEM_DATA[group]['room'], group)
    
      elif typus == "alexa":
        dev, sender = content.split(',')
        loud        = 3
        R           = ELEM_DATA[group]['room']

        if value == 0: alexa_speak(dev, "-", loud*10, "pause", R, 2)
        if value == 1: alexa_speak(dev, "-", loud*10, sender,  R, 2)

      else:
        raise Exception("Error 2 in Macro " + group + " " + M)

#########################
#       DURATION	#
#########################
def duration(input_T, accu="normal"):

  delta_T = input_T

  # ------------------------------------
  # break down into days, hors, min, sec
  # ------------------------------------
  t_o = DT.datetime.fromtimestamp(time.time() - input_T)
  t_n = DT.datetime.fromtimestamp(time.time())

  seconds = t_n.second  - t_o.second
  minutes = t_n.minute  - t_o.minute
  hours   = t_n.hour    - t_o.hour
  days    = t_n.day     - t_o.day
  month   = t_n.month   - t_o.month
  years   = t_n.year    - t_o.year

  if seconds < 0:
    seconds += 60
    minutes -=  1
  if minutes < 0:
    minutes += 60
    hours   -=  1
  if hours < 0:
    hours  += 24
    days   -= 1
  if days < 0:
    prev_month = t_n.replace(day=1) - DT.timedelta(days=1)
    days   += calendar.monthrange(prev_month.year, prev_month.month)[1]
    month  -= 1
  if month < 0:
    month  += 12
    years  -= 1

  if accu == "full":
    output = ""
    if years > 0:
      if   years == 1: output += "1 Jahr "
      else:            output += "{:d} Jahren ".format(years)
  
    if month > 0:
      if   month == 1: output += "1 Monat "
      else:            output += "{:d} Monaten ".format(month)
  
    if days > 0:
      if   days == 1:  output += "1 Tag "
      else:            output += "{:.0f} Tagen ".format(days)
  
    if hours > 0:
      if hours     == 1: output += "1 Stunde "
      else:              output += "{:.0f} Stunden ".format(hours)
  
    if minutes > 0:
      if minutes == 1: output += "1 Minute "
      else:            output += "{:.0f} Minuten ".format(minutes)
  
    if seconds > 0:
      if seconds == 1: output += "1 Sekunde"
      else:            output += "{:.0f} Sekunden".format(seconds)
  
    return output

  # remember initial=exact values before applying rounding
  seconds0 = seconds
  minutes0 = minutes
  hours0   = hours
  days0    = days
  month0   = month
  years0   = years

  # ------------------------------------
  # round small / high numbers
  # ------------------------------------
  if (minutes > 0) and (seconds < 10): seconds = 0

  if seconds > 50:
    seconds = 0
    minutes += 1

  if ((hours  >  0) and (minutes <  5)) or \
     ((hours  >  3) and (minutes < 10)) or \
     ((hours  >  7) and (minutes < 15)):
    minutes = 0
    seconds = 0

  if ((hours  >  0) and (minutes > 55)) or \
     ((hours  >  2) and (minutes > 50)) or \
     ((hours  >  7) and (minutes > 45)):
    minutes = 0
    seconds = 0
    hours   += 1

  if (days   > 0) and (hours   <  3): hours   = 0

  if (days   > 0) and (hours   > 21):
    hours   = 0
    days    += 1

  if   years > 0:
    if days > 15:
      month += 1
      days   = 0
    else:
      days   = 0

  elif month > 0:
    if hours > 12:
      days += 1
      hours = 0
    else:
      hours = 0

  elif days  > 0:
    if minutes >= 30:
      hours += 1
      minutes= 0
    else:
      minutes= 0

  elif hours > 0:
    if seconds >= 30:
      minutes += 1
      seconds  = 0
    else:
      seconds  = 0

  elif minutes > 0:
    if seconds >= 40:
      minutes += 1
      seconds  = 0

  if (hours  > 1):
    min10 = int((minutes+5.0)/10.)*10
    min15 = int((minutes+7.5)/15.)*15
    if abs(min15 - minutes) < abs(min10 - minutes):
      minutes = min15
    else:
      minutes = min10
    seconds = 0

  # corrections
  if minutes >= 60:
    minutes -= 60
    hours   += 1
  if hours >= 24:
    hours   -= 24
    days    += 1
  prev_month = t_n.replace(day=1) - DT.timedelta(days=1)
  prev_days  = calendar.monthrange(prev_month.year, prev_month.month)[1]
  if days  > prev_days:
    days    -= prev_days
    month   += 1
  if month >= 12:
    month   -= 12
    years   += 1

  # adjust accuracy
  if accu == "low":
    
    if minutes > 0:
      seconds = ((seconds+15) // 30) * 30
      if (seconds == 60) or ((minutes > 3) and (seconds == 30)):
        if seconds0 >= 30: minutes  += 1
        seconds   = 0

    if hours > 0:
      minutes = ((minutes+15) // 30) * 30
      if (minutes == 60) or ((hours > 3) and (minutes == 30)):
        if minutes0 >= 30: hours   += 1
        minutes  = 0

    if days > 0:
      hours = ((hours+6) // 12) * 12
      if (hours == 24) or ((days > 3) and (hours == 12)):
        if hours0 >= 12: days  += 1
        hours  = 0
    
    if month > 0:
      days = ((days+7) // 15) * 15
      if (days == 30) or ((month > 4) and (days == 15)):
        if days0 >= 15: month += 1
        days   = 0
    
    if years > 0:
      month = ((month+3) // 6) * 6
      if (month == 12) or ((years > 3) and (month == 6)):
        if month0 >= 6: years += 1
        month  = 0
    
    if (years == 0) and (month > 9) and (days == 0):
      years += 1
      month  = 0
  
    if (month == 0) and (days > 20) and (hours == 0):
      month += 1
      days   = 0
 
    if (days == 0) and (hours > 18) and (minutes == 0):
      days  += 1
      hours  = 0

    if (days == 0) and (9 < hours <= 18) and (minutes == 0):
      hours  = 12
 
    if (hours == 0) and (minutes > 44) and (seconds == 0):
      hours   += 1
      minutes  = 0
 
    if (hours == 0) and (20 < minutes <= 44) and (seconds == 0):
      minutes  = 30
 
  # ------------------------------------
  # convert to text
  # ------------------------------------
  if   years > 0:
    if   years == 1: output = "einem Jahr und "
    else:            output = "{:d} Jahren und ".format(years)
    if   month == 0: output = output.replace(' und ', '')
    elif month == 1: output = output + "einem Monat".format(month)
    elif 4 < month < 8:
      output = output.replace('einem Jahr und ', 'ein einhalb Jahren')
      output = output.replace(' Jahren und ', ' einhalb Jahren')
    else:            output = output + "{:d} Monaten".format(month)

  elif month > 0:
    if   month == 1: output = "einem Monat und "
    else:            output = "{:d} Monaten und ".format(month)
    if   days  == 0: output = output.replace(' und ', '')
    elif days  == 1: output = output + "einem Tag".format(days)
    elif 12 < days < 18:
      output = output.replace('einem Monat und ', 'ein einhalb Monaten')
      output = output.replace(' Monat und ', ' einhalb Monaten')
    else:            output = output + "{:d} Tagen".format(days)

  elif days > 0:
    if   days == 1:  output = "einem Tag und "
    else:            output = "{:.0f} Tagen und ".format(days)
    if   hours == 0: output = output.replace(' und ', '')
    elif hours == 1: output = output + "einer Stunde".format(hours)
    elif 9 < hours < 15:
      output = output.replace('einem Tag und ', 'ein einhalb Tagen')
      output = output.replace(' Tagen und ', ' einhalb Tagen')
    else:            output = output + "{:.0f} Stunden".format(hours)

  elif hours > 0:
    if hours     == 1: output = "einer Stunde und "
    else:              output = "{:.0f} Stunden und ".format(hours)
    if   minutes == 0: output = output.replace(' und ', '')
    elif minutes == 1: output = output + "einer Minute"
    elif 24 < minutes < 36:
      output = output.replace('einer Stunde und ', 'ein einhalb Stunden')
      output = output.replace(' Stunden und ', ' einhalb Stunden')
    else:            output = output + "{:.0f} Minuten".format(minutes)
    if (hours == 12) and (accu == "low"): output = " einem halben Tag "

  elif minutes > 0:
    if minutes == 1: output = "einer Minute"
    elif 24 < minutes < 36: output = "einer halben Stunde"
    else:            output = "{:.0f} Minuten".format(minutes)
    if 24 < seconds < 36:
      output = output.replace('einer Minute', 'ein einhalb Minuten')
      output = output.replace(' Minuten', ' einhalb Minuten')

  else:
    if seconds == 1: output = "einer Sekunde"
    else:            output = "{:.0f} Sekunden".format(seconds)

  return output

def check_keep_alive():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm

  for E in ELEM_DATA:
    type  = ELEM_DATA[E]["type"]
    keep  = keep_alive_time[type]
    try:  alive = time.time() - ELEM_DATA[E]["time"]
    except:
      verbose_print(1,"error in -time- on element " + E)
      ELEM_DATA[E]["time"] = time.time()
      alive = 0.0

    if (keep > 0.0) and (60.0*60.0 > alive > keep * 60.0):
      verbose_print(1,"keep alive exceeded for {:s} {:s} of {:s} with keep {:.0f} min to actual {:.0f} minutes.".format( \
                        E, ELEM_DATA[E]['name'], type, keep, alive/60.0))
      alarm = copy.deepcopy(ALARM_OBJ)
      alarm["prio"] = 3
      alarm["time"] = time.time()
      alarm["type"] = ELEM_DATA[E]["type"]
      alarm["level"] = 3 if not E in conf_data['alarm2call'] else 0
      alarm["reason"] = "not_alive"
      alarm["action"] = "check"
      alarm["group"] = E
      element_alarm(alarm['group'],alarm['prio'],alarm['level'],alarm['reason'],alarm['action'])

    try:    x = ELEM_DATA[E]["alarm"]["reason"]
    except: ELEM_DATA[E]["alarm"] = copy.deepcopy(ALARM_OBJ)

    if ((keep < 0.0) or ((keep > 0.0) and (alive < keep * 60.0))) and (ELEM_DATA[E]["alarm"]["reason"] == "not_alive"):
      verbose_print(6,"keep alive supported for {:s} of {:s} with keep {:.0f} min to actual {:.0f} minutes.".format(E, type, keep, alive/60.0))
      alarm = copy.deepcopy(ALARM_OBJ)
      alarm["prio"] = 3
      alarm["time"] = time.time()
      alarm["type"] = ELEM_DATA[E]["type"]
      alarm["level"] = 4
      alarm["reason"] = "none"
      alarm["action"] = "none"
      alarm["group"] = E
      element_alarm(alarm['group'],alarm['prio'],alarm['level'],alarm['reason'],alarm['action'])

def dict_pretty(d, tab=0):
    s = ['{\n']
    for k,v in list(d.items()):
        if isinstance(v, dict):
            v = dict_pretty(v, tab+1)
        else:
            v = repr(v)

        s.append('%s%r: %s,\n' % ('&nbsp;'*tab*4, k, v))
    s.append('%s}' % ('&nbsp;'*tab*4))
    return ''.join(s)

def show_eib_adr():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm

  adr_f = '/var/www/ehome-cgi-bin/eib_adr.txt'
  out_f = '/var/www/ehome-html/eib_adr.html'

  if not os.path.isfile(adr_f):
    return

  f = open(adr_f, 'r')
  adr = f.readline()
  adr = adr.strip()
  f.close()
  verbose_print(1,"processing adr " + adr)
  os.remove(adr_f)

  f = open(out_f, 'w')
  dash_mode = "alexa"

  zeit = datetime.now().strftime("%Y.%m.%d at %H:%M:%S")
  out  = "<font face=verdana><center><h1>{:s} on {:s}</h1></center>&nbsp;<p>".format(adr, zeit)
  if adr in ELEM_DATA:
    pE  = dict_pretty(ELEM_DATA[adr])
    pE = pE.replace('\n', '<br>\n')
    pE = pE.replace(' ', '&nbsp;') + "<p>\n"
    out += pE
    out += "last action   {:11.1f} {:s}".format((time.time() - ELEM_DATA[adr]["time"])/60.0, "min ago") + "<br>\n"
    out += "last alarm    {:11.1f} {:s}".format((time.time() - ELEM_DATA[adr]['alarm']["time"])/60.0, "min ago") + "<br>\n"
    out += "blocked since {:11.1f} {:s}".format((time.time() - ELEM_DATA[adr]['block']["time"])/60.0, "min ago") + "<br>\n"
    if ELEM_DATA[adr]['block']["until"] - time.time() > 0:
      out += "blocked until {:11.1f} {:s}".format((ELEM_DATA[adr]['block']["until"] - time.time())/60.0, "min in the future") + "<br>\n"
    else:
      out += "blocked until {:11.1f} {:s}".format((time.time() - ELEM_DATA[adr]['block']["until"])/60.0, "min in the past") + "<br>\n"
    out += "<br>\n"
    out += "ROOM_DATA room {:d} alarm:".format(ELEM_DATA[adr]['room']) + "<br>\n"
    out += str(ROOM_DATA[ELEM_DATA[adr]['room']]['alarm']) + "<br>\n"
    out += "<br>\n"
  
  else:
    i = 0
    for E in ELEM_DATA:
      if ELEM_DATA[E]['alarm']['level'] < 4:
        out += ("Alarm in {:s} {:s}".format(E, ELEM_DATA[E]['name']) + "<br>\n")
        i += 1
    out += "Anzahl Alarme in ELEMENTS: {:d}".format(i) + "<br>\n"
    out += "<br>\n"
  
    i = 0
    for R in ROOM_DATA:
      if ROOM_DATA[R]['alarm']['level'] < 4:
        out += "Alarm in {:d} {:s}".format(R, ROOM_DATA[R]['name']) + "<br>\n"
        i += 1
    out += "Anzahl Alarme in ROOMS : {:d}".format(i) + "<br>\n"
    out += "<br>\n"
  
    if FLAT_DATA['alarm']['prio'] < 4:
      out += "Alarm in flat {:s}".format(E, FLAT_DATA['alarm']['group']) + "<br>\n"
    else:
      out += "Kein Alarm in Flat" + "<br>\n"
  out += "<br>\n"
  
  out += "====================================================<br>\n"
  out += dash_all("details") + "<br>\n"
  out += "====================================================<br>\n"
  out += dash_alarm("details") + "<br>\n"
  out += "====================================================<br>\n"
  
  out += "<br>\n"
  out += "CLIENTS online<br>\n"
  clients = 0
  for E in ELEM_DATA:
    try:
      if (ELEM_DATA[E]["type"] == "client") and (ELEM_DATA[E]["act"] == 1):
        out += E + ELEM_DATA[E]["act"] + ELEM_DATA[E]['name'] + "<br>\n"
        clients += 1
    except:
      pass
  out += str(clients) + " online<br>\n"
  out += "<br>\n"
  
  out += "SERVERS offline<br>\n"
  servers = 0
  for E in ELEM_DATA:
    try:
      if (ELEM_DATA[E]["type"] == "server") and (ELEM_DATA[E]["act"] == 0):
        out += E + ELEM_DATA[E]["act"] + ELEM_DATA[E]['name'] + "<br>\n"
        servers += 1
    except:
      pass

  out += str(servers) + " offline<br>\n"
  out += "servers offline in flat " + str(FLAT_DATA["server"]["act"]) + "<br>\n"
  out += "<br>\n"
  
  out += "persons in flat: " + str(FLAT_DATA["person"]["act"]) + "<br>\n"
  out += "<br>\n"
  
  out += "sun position: " + str(sun_position(datetime.now())) + "<br>\n"
  out += "</font>"

  out = out.replace('ä', '&auml;')
  out = out.replace('ö', '&ouml;')
  out = out.replace('ü', '&uuml;')
  out = out.replace('Ä', '&Auml;')
  out = out.replace('Ö', '&Ouml;')
  out = out.replace('Ü', '&Uuml;')
  out = out.replace('ß', '&szlig;')

  f.write(out)
  f.close()

wetter_text     = {
0  : "Trocken",
1  : "Leichter Regen",
2  : "Regen",
3  : "Starker Regen"
}

wetter_codes    = {
#code     Text                                      Icon   Dh
200: ["Gewitter mit leichtem Regen"      , " 11d", dh_Niesel, ds_none  ],
201: ["Gewitter mit Regen"               , " 11d", dh_Regen , ds_none  ],
202: ["Gewitter mit starkem Regen"       , " 11d", dh_heavy , ds_none  ],
210: ["leichtes Gewitter"                , " 11d", dh_Niesel, ds_none  ],
211: ["Gewitter"                         , " 11d", dh_norm  , ds_none  ],
212: ["starkes Gewitter"                 , " 11d", dh_norm  , ds_none  ],
221: ["extremes Gewitter"                , " 11d", dh_norm  , ds_none  ],
230: ["Gewitter mit leichtem Niesel"     , " 11d", dh_Niesel, ds_none  ],
231: ["Gewitter mit Niesel"              , " 11d", dh_Niesel, ds_none  ],
232: ["Gewitter mit starkem Niesel"      , " 11d", dh_Niesel, ds_none  ],
300: ["leichter Niesel"                  , " 09d", dh_Regen , ds_none  ],
301: ["Niesel"                           , " 09d", dh_Regen , ds_none  ],
302: ["sehr intensiver Niesel"           , " 09d", dh_Regen , ds_none  ],
310: ["leichter Nieselregen"             , " 09d", dh_Niesel, ds_none  ],
311: ["Nieselregen"                      , " 09d", dh_Niesel, ds_none  ],
312: ["sehr intensiver Nieselregen"      , " 09d", dh_Niesel, ds_none  ],
313: ["Regenschauer und Niesel"          , " 09d", dh_Niesel, ds_none  ],
314: ["starke Regenschauer und Niesel"   , " 09d", dh_Regen , ds_none  ],
321: ["Nieselregen und Schauer"          , " 09d", dh_Niesel, ds_none  ],
500: ["leichter Regen"                   , " 10d", dh_Regen , ds_none  ],
501: ["moderater Regen"                  , " 10d", dh_Regen , ds_none  ],
502: ["sehr intensiver Regen"            , " 10d", dh_heavy , ds_none  ],
503: ["sehr starker Regen"               , " 10d", dh_heavy , ds_none  ],
504: ["extremer Regen"                   , " 10d", dh_heavy , ds_none  ],
511: ["frierender Regen"                 , " 13d", dh_Regen , ds_none  ],
520: ["leichter Regenschauer"            , " 09d", dh_Regen , ds_none  ],
521: ["Regenschauer"                     , " 09d", dh_Regen , ds_none  ],
522: ["sehr intensiver Regenschauer"     , " 09d", dh_Regen , ds_none  ],
531: ["extreme Regenschauer"             , " 09d", dh_Regen , ds_none  ],
600: ["leichter Schnee"                  , " 13d", dh_Regen , ds_none  ],
601: ["Schnee"                           , " 13d", dh_Regen , ds_none  ],
602: ["starker Schnee"                   , " 13d", dh_Regen , ds_none  ],
611: ["Schneeregen"                      , " 13d", dh_Regen , ds_none  ],
612: ["Schneeregenschauer"               , " 13d", dh_Regen , ds_none  ],
615: ["leichter Regen und Schnee"        , " 13d", dh_Regen , ds_none  ],
616: ["Regen und Schnee"                 , " 13d", dh_Regen , ds_none  ],
620: ["leichte Schneeschauer"            , " 13d", dh_Niesel, ds_none  ],
621: ["Schneeschauer"                    , " 13d", dh_Niesel, ds_none  ],
622: ["starke Schneeschauer"             , " 13d", dh_Niesel, ds_none  ],
701: ["Neben"                            , " 50d", dh_norm  , ds_na    ],
711: ["Rauch"                            , " 50d", dh_norm  , ds_na    ],
721: ["Dunst"                            , " 50d", dh_norm  , ds_na    ],
731: ["Sand und Staubwirbel"             , " 50d", dh_norm  , ds_na    ],
741: ["Nebel"                            , " 50d", dh_norm  , ds_na    ],
751: ["Sand"                             , " 50d", dh_norm  , ds_na    ],
761: ["Staub"                            , " 50d", dh_norm  , ds_na    ],
762: ["vulkanische Asche"                , " 50d", dh_norm  , ds_na    ],
771: ["Böen"                             , " 50d", dh_norm  , ds_na    ],
781: ["Tornado"                          , " 50d", dh_norm  , ds_na    ],
800: ["klarer Himmel"                    , " 01d", dh_norm  , ds_full  ],
801: ["leicht bewölkt"                   , " 02d", dh_norm  , ds_full  ],
802: ["aufgelockerte Bewölkung"          , " 03d", dh_norm  , ds_moder ],
803: ["aufgelockerte Bewölkung"          , " 04d", dh_norm  , ds_moder ],
804: ["bewölkt"                          , " 04d", dh_norm  , ds_moder ]
}

