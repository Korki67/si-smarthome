# -*- coding: utf-8 -*-

#########################
#     WINDOW		#
#########################
def update_window():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['window']

  # count number of open windows in room & flat
  # value 0=closed // 1=open
  num_windo = 0
  all_windo = 0
  Room  = ELEM_DATA[knx_group]["room"]
  for i_group in ELEM_DATA:
    if ELEM_DATA[i_group]["type"] == "window":
      all_windo += (ELEM_DATA[i_group]["act"] > 0)
      if ELEM_DATA[i_group]["room"] == Room:
        num_windo += (ELEM_DATA[i_group]["act"] > 0)

  ROOM_DATA[Room]["window"]["num"]  = num_windo
  ROOM_DATA[Room]["window"]["time"] = knx_time
  FLAT_DATA["window"]["act"]  = all_windo
  FLAT_DATA["window"]["time"] = knx_time

  verbose_print (V, "windows: " + str(num_windo) + " in rooms:" + str(Room))

  # call routine to open door at window if listed in config
  if knx_group in conf_data['Doors']: door_open(knx_group)

#########################
#     AMBIENT PRESS	#
#########################
def update_amb_p():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['amb_p']

  FLAT_DATA["amb_p"]["act"]  = knx_act
  FLAT_DATA["amb_p"]["time"] = knx_time

#########################
#     	HEAT		#
#########################
def update_heat():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['heat']

  # count number of heaters/radiators in operation in room & flat
  # value 0=off // 1=heating
  num_heat = 0
  all_heat = 0
  Room = ELEM_DATA[knx_group]["room"]
  for i_group in ELEM_DATA:
    if ELEM_DATA[i_group]["type"] == "heat":
      all_heat += (ELEM_DATA[i_group]["act"] > 0)
      if ELEM_DATA[i_group]["room"] == Room:
        num_heat += (ELEM_DATA[i_group]["act"] > 0)

  ROOM_DATA[Room]["heat"]["num"]  = num_heat
  ROOM_DATA[Room]["heat"]["time"] = knx_time
  FLAT_DATA["heat"]["act"]  = all_heat
  FLAT_DATA["heat"]["time"] = knx_time

  verbose_print (V, f"heatings on: {all_heat:d}")

#########################
#     	MOTION		#
#########################
def update_motion():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['motion']

  # store time of motion in room and flat
  # value 1=motion start // 0=motion end
  Room = ELEM_DATA[knx_group]["room"]
  ROOM_DATA[Room]["motion"]["time"] = knx_time
  FLAT_DATA["motion"]["time"]       = knx_time

  verbose_print (V, f"Motion in {Room:d} {ROOM_DATA[Room]['name']:s}")

#########################
#     	WATER		#
#########################
def update_water():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['water']

  # store value & time of water sensor in room
  Room = ELEM_DATA[knx_group]["room"]
  ROOM_DATA[Room]["water"]["act"]  = knx_act
  ROOM_DATA[Room]["water"]["time"] = knx_time

  # find most critical in time or value to store in flat
  # value 0=water alarm,   1=OK
  c_act   =  2
  c_time  = knx_time + 60
  c_group = '9/0/99'
  for E in conf_data['Type_Lists']['water_sensors'].split(','):
    if (c_act == 0):
      if ((ELEM_DATA[E]['act'] == 0) and (ELEM_DATA[E]['time'] < c_time)):
        c_act   = ELEM_DATA[E]['act']
        c_time  = ELEM_DATA[E]['time']
        c_group = E
    elif ELEM_DATA[E]['act'] == 0:
      c_act   = ELEM_DATA[E]['act']
      c_time  = ELEM_DATA[E]['time']
      c_group = E
    elif (ELEM_DATA[E]['time'] < c_time) and (ELEM_DATA[E]['act'] != -1):
      c_act   = ELEM_DATA[E]['act']
      c_time  = ELEM_DATA[E]['time']
      c_group = E

  FLAT_DATA["water"]["time"]    = c_time
  FLAT_DATA["water"]["act"]     = c_act
  FLAT_DATA["water"]["trigger"] = c_group

  if   (c_act ==  1):
    verbose_print (V, f"No water in flat.")
  else:
    verbose_print (1, f"Alarm about water in room {Room:d} {ROOM_DATA[Room]['name']:s}.")

#########################
#     SWITCH		#
#########################
def update_switch():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['switch']

  # count number of switches "on"
  num_switch = 0
  all_switch = 0
  Room = ELEM_DATA[knx_group]["room"]
  for i_group in ELEM_DATA:
    if ELEM_DATA[i_group]["type"] == "switch":
      all_switch += (ELEM_DATA[i_group]["act"] > 0)
      if ELEM_DATA[i_group]["room"] == Room:
        num_switch += (ELEM_DATA[i_group]["act"] > 0)

  ROOM_DATA[Room]["switch"]["num"] = num_switch
  ROOM_DATA[Room]["switch"]["time"] = knx_time
  FLAT_DATA["switch"]["act"] = all_switch
  FLAT_DATA["switch"]["time"] = knx_time

  verbose_print (V, f"switches on: {all_switch:d}")

#########################
#     BEAUFORT		#
#########################
def update_beauf():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['beauf']

  aver = knx_act   / 10.0
  maxi = knx_alter / 10.0

  try:    debug = conf_data["Debug"][ELEM_DATA[knx_group]["type"]]
  except: debug = 0

  if knx_group == "1/2/6":
    if debug:
      aver = 90.2
      maxi = 130.1
    FLAT_DATA['beauf']["speed_av"] = aver
    FLAT_DATA['beauf']["speed_mx"] = maxi
  else:
    if debug:
      aver = 7.2
      maxi = 9.1
    FLAT_DATA['beauf']["beauf_av"] = aver
    FLAT_DATA['beauf']["beauf_mx"] = maxi

  FLAT_DATA['beauf']["time"] = knx_time

  verbose_print (V, f"wind speed average: {aver:.1f} max: {maxi:.1f} from {knx_group:s}")

#########################
#     INTERNET		#
#########################
def update_inter():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['inter']

  FLAT_DATA['inter']['act'] = knx_act

#########################
#       SPEED		#
#########################
def update_speed():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['speed']

  # ID = PING, DOWN, UPLO
  id = ELEM_DATA[knx_group]['ID']
  if id == "PING": knx_act = knx_act / 10.0
  FLAT_DATA["speed"][id]     = knx_act
  FLAT_DATA["speed"]["time"] = knx_time

  if id == "UPLO": verbose_print (V, f"internet speed: "	+ \
      f"{FLAT_DATA['speed']['PING']:.1f} ping, "		+ \
      f"{FLAT_DATA['speed']['DOWN']:d} down, "			+ \
      f"{FLAT_DATA['speed']['UPLO']:d} uplod in Mbit/s")

#########################
#     GARAGE		#
#########################
def update_garage():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['garage']

  # find garage door open the longest
  # value 0=open // 1=closed
  longest_open = '9/0/99'
  longest_time = 0
  for E in conf_data['Type_Lists']['garages'].split(','):
    if ELEM_DATA[E]["act"] == 0:
      if knx_time - ELEM_DATA[E]["time"] > longest_time:
        longest_time = knx_time - ELEM_DATA[E]["time"]
        longest_open = E
  FLAT_DATA["garage"]["act"]  = E
  FLAT_DATA["garage"]["time"] = longest_time

  if longest_open != '9/0/99':
    verbose_print(V,'garage ' + knx_group + ' value ' + str(knx_act))
    if longest_time > 10.0*60.0:
      verbose_print(1,f"Garage {ELEM_DATA[longest_open]['name']:s} open since {longest_time:.0f} sec")

#########################
#     CO2		#
#########################
def update_CO2():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['CO2']
  room = ELEM_DATA[knx_group]["room"]
  ROOM_DATA[room]['CO2']['act']  = knx_act

  # anlalyze flag for CO2 levels
  if knx_act > 400:
    try:
      yel = conf_data['Room'+str(room)]['CO2_yellow']
      red = conf_data['Room'+str(room)]['CO2_red']
    except:
      yel = conf_data['CO2']['CO2_yellow']
      red = conf_data['CO2']['CO2_red']

    flag = "green"
    if knx_act > yel: flag = "yellow"
    if knx_act > red: flag = "red"

    if flag != ELEM_DATA[knx_group]['flag']:
      ELEM_DATA[knx_group]['flag']   = flag
      ELEM_DATA[knx_group]['time']   = knx_time
      ROOM_DATA[room]['CO2']['flag'] = flag
      ROOM_DATA[room]['CO2']['time'] = knx_time

  else:
    ROOM_DATA[room]['CO2'] = {'act': 400, 'time': knx_time, 'flag': "gray"}

  # analyze CO2 in flat for all the rooms
  # there is not act(ual) for the flat, use of max in "act"
  # average and minimum of CO2 are of no interest, not used
  CO2_Max = 0
  CO2_Ele = '9/0/99'
  CO2_Flg = 'green'
  for E in conf_data['Type_Lists']['CO2'].split(','):
    if ELEM_DATA[E]['act'] > CO2_Max:
      CO2_Max = ELEM_DATA[E]['act']
      CO2_Flg = ELEM_DATA[E]['flag']
      CO2_Ele = E

  FLAT_DATA['CO2']['act']   = CO2_Max
  FLAT_DATA['CO2']['group'] = CO2_Ele
  if CO2_Flg != FLAT_DATA['CO2']['flag']:
    FLAT_DATA['CO2']['time']  = knx_time
    FLAT_DATA['CO2']['flag']  = CO2_Flg

#########################
#     FRIDGES
#########################
def update_fridge():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['fridge']
  room = ELEM_DATA[knx_group]["room"]

  knx_act = (knx_act / 10.0) - 50.0
  if   knx_alter == 0:
    ELEM_DATA[knx_group]['act'] = knx_act
  elif knx_alter == 1:
    ELEM_DATA[knx_group]['min'] = knx_act
  elif knx_alter == 2:
    ELEM_DATA[knx_group]['max'] = knx_act
  else: raise Exception(f"Unzulaessiger Wert alter {knx_alter} in fridge {knx_group}")

  # anlalyze most severe fridge
  if knx_alter == 2:
    try:    x = (ELEM_DATA[knx_group]['act'] - ELEM_DATA[knx_group]['min']) / (ELEM_DATA[knx_group]['max'] - ELEM_DATA[knx_group]['min'])
    except: x = 0.5
    flag  = "green"
    if x > 1.1: flag = "yellow"
    if x > 1.3: flag = "red"
    ELEM_DATA[knx_group]['flag'] = flag
    ELEM_DATA[knx_group]['time'] = knx_time

    x_max = -1.0
    g_max = '9/0/99'
    flag  = "green"
    for F in conf_data['Type_Lists']['fridge'].split(','):
      try:    x = (ELEM_DATA[F]['act'] - ELEM_DATA[F]['min']) / (ELEM_DATA[F]['max'] - ELEM_DATA[F]['min'])
      except: x = 0.5
      if x > x_max:
        x_max = x
        g_max = F
        flag = ELEM_DATA[F]['flag']
  
    if (FLAT_DATA['fridge']['group'] != g_max) or (FLAT_DATA['fridge']['flag'] != flag):
      FLAT_DATA['fridge']['time']  = knx_time

    FLAT_DATA['fridge']['flag']  = flag
    FLAT_DATA['fridge']['group'] = knx_group

#########################
#     CENTHEAT		#
#########################
def update_centheat():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['centheat']
  room = ELEM_DATA[knx_group]["room"]

  knx_act = (knx_act / 10.0) - 50.0
  if   knx_alter == 0:
    ELEM_DATA[knx_group]['act'] = knx_act
  elif knx_alter == 1:
    ELEM_DATA[knx_group]['min'] = knx_act
  elif knx_alter == 2:
    ELEM_DATA[knx_group]['max'] = knx_act
  else: raise Exception(f"Unzulaessiger Wert alter {knx_alter} in fridge {knx_group}")

  if knx_alter == 2:
    try:    x = (ELEM_DATA[knx_group]['act'] - ELEM_DATA[knx_group]['min']) / (ELEM_DATA[knx_group]['max'] - ELEM_DATA[knx_group]['min'])
    except: x = 0.5
    flag  = "green"
    if x > 1.1: flag = "yellow"
    if x > 1.3: flag = "red"
    ELEM_DATA[knx_group]['flag'] = flag
    ELEM_DATA[knx_group]['time'] = knx_time

  # anlalyze most severe temperature of heating
  # water temp 1/2/16 max=2 is the last one to come
  if (knx_group == '1/2/16') and (knx_alter == 2):
    x_min = 2.0
    g_min = '9/0/99'
    flag  = "green"
    for T in conf_data['Type_Lists']['centheat'].split(','):
      try:    x = (ELEM_DATA[T]['act'] - ELEM_DATA[T]['min']) / (ELEM_DATA[T]['max'] - ELEM_DATA[T]['min'])
      except: x = 0.5
      if x < x_min:
        x_min = x
        g_min = T
        flag = ELEM_DATA[T]['flag']
  
    if (FLAT_DATA['centheat']['group'] != g_min) or (FLAT_DATA['centheat']['flag'] != flag):
      FLAT_DATA['fridge']['time']  = knx_time

    FLAT_DATA['centheat']['flag']  = flag
    FLAT_DATA['centheat']['group'] = knx_group

#########################
#  decode KNX TEMP	#
#########################
def calc_temp(t):

  # decode KNX bit-coded float temperature

  # HEX in INT
  i = int(t, 16);
  # SIGN
  s = i // 2**15;
  # MANT
  e = i & (2**15 - 1);
  e = e // 2**11;
  # EXP
  m = i & (2**11 - 1);
  tem = float(1-2*s) * float(m) * 0.01 * float(2**e);
  return tem

#########################
#  room temperature	#
#########################
def update_temp():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time, knx_read

  V = conf_data['Verbosity']['temp']

  room_temp_array = [0, 10, 11, 12, 13]

  try:    temp = calc_temp(knx_read[5] + knx_read[6])
  except: temp = calc_temp(knx_read[5])

  if temp < 5.0:
    verbose_print(1,"Error Temp " + knx_group + " " + str(knx_read))
    return

  Room  = ELEM_DATA[knx_group]["room"]
  ROOM_DATA[Room]["temp"]["act"]  = temp
  ROOM_DATA[Room]["temp"]["time"] = time.time()
  knx_act = temp

  # find average for flat and min/max
  temp_ave = 0.0
  temp_min = 100.0
  temp_max = -10.0
  temp_num = 0
  for i_group in ELEM_DATA:
    if (0 < ELEM_DATA[i_group]["room"] < 10) \
	and (ELEM_DATA[i_group]["type"] == "temp") \
	and (0.0 < ELEM_DATA[i_group]["act"] < 99.0):
      temp_ave = temp_ave + ELEM_DATA[i_group]["act"]
      if temp_min > ELEM_DATA[i_group]["act"]:
        temp_min = ELEM_DATA[i_group]["act"]
        elem_min = i_group
      if temp_max < ELEM_DATA[i_group]["act"]:
        temp_max = ELEM_DATA[i_group]["act"]
        elem_max = i_group
      temp_num += 1
  if temp_num > 0:
    temp_ave = int(0.5 + temp_ave / float(temp_num))
    FLAT_DATA["temp"]["act"]  = temp_ave
    FLAT_DATA["temp"]["minV"] = temp_min
    FLAT_DATA["temp"]["minE"] = elem_min
    FLAT_DATA["temp"]["maxV"] = temp_max
    FLAT_DATA["temp"]["maxE"] = elem_max
  else:
    FLAT_DATA["temp"]["act"] = -1.0
  FLAT_DATA["temp"]["time"] = time.time()
  
  verbose_print (V, f"Temperature room {Room:d} of {temp:.1f}, average flat {temp_ave:.1f}")

#########################
#     LIGHT		#
#########################
def update_light():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['light']

  # count number of lights "on"
  # value 0=off // 1=on
  num_light = 0
  all_light = 0
  Room = ELEM_DATA[knx_group]["room"]
  for i_group in ELEM_DATA:
    if ELEM_DATA[i_group]["type"] == "light":
      all_light += (ELEM_DATA[i_group]["act"] > 0)
      if ELEM_DATA[i_group]["room"] == Room:
        num_light += (ELEM_DATA[i_group]["act"] > 0)

  ROOM_DATA[Room]["light"]["no"] = num_light
  ROOM_DATA[Room]["light"]["time"] = knx_time
  ROOM_DATA[Room]["time"] = knx_time
  FLAT_DATA["light"]["act"] = all_light
  FLAT_DATA["light"]["num"] = all_light
  FLAT_DATA["light"]["time"] = time.time()
  verbose_print (V, f"lights: {num_light:d} in Rooms {Room:d}, total {all_light:d} in flat.")

  if knx_group in conf_data["Type_Lists"]["balconies"].split(','):
    blinds_auto_away(knx_group)

#########################
#     SERVER		#
#########################
def update_server():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['server']

  # count number of offline servers and find oldest one
  # value 0=offline // 1=online
  num_errors = 0
  all_errors = 0
  tim_errors = knx_time + 60
  ele_errors = '9/0/99'
  Room  = ELEM_DATA[knx_group]["room"]
  for i_group in ELEM_DATA:
    if ELEM_DATA[i_group]["type"] == "server":
      if ELEM_DATA[i_group]["act"] == 0:
        all_errors += 1
        if ELEM_DATA[i_group]["room"] == Room:
          num_errors += 1
        if ELEM_DATA[i_group]["time"] < tim_errors:
          tim_errors = ELEM_DATA[i_group]["time"]
          ele_errors = i_group
        verbose_print (V, "server error: " + i_group + " " + ELEM_DATA[i_group]["ID"])

  ROOM_DATA[Room]["server"]["act"]  = num_errors
  ROOM_DATA[Room]["server"]["num"]  = num_errors
  ROOM_DATA[Room]["server"]["time"] = knx_time
  FLAT_DATA["server"]["act"]   = all_errors
  FLAT_DATA["server"]["num"]   = all_errors
  FLAT_DATA["server"]["time"]  = tim_errors
  FLAT_DATA["server"]["group"] = ele_errors

  verbose_print (V, "servers offline: " + str(all_errors) + " in flat")

#########################
#     CLIENT		#
#########################
def update_client():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['client']

  # count number of online clients and find newest one
  # value 0=offline // 1=online
  num_errors = 0
  all_errors = 0
  tim_errors = 0
  ele_errors = '9/0/99'
  Room  = ELEM_DATA[knx_group]["room"]
  for i_group in ELEM_DATA:
    if ELEM_DATA[i_group]["type"] == "client":
      if ELEM_DATA[i_group]["act"] == 1:
        all_errors += 1
        if ELEM_DATA[i_group]["room"] == Room:
          num_errors += 1
        if ELEM_DATA[i_group]["time"] > tim_errors:
          tim_errors = ELEM_DATA[i_group]["time"]
          ele_errors = i_group
        verbose_print (V, "client online: " + i_group + " " + ELEM_DATA[i_group]["ID"])

  ROOM_DATA[Room]["client"]["act"]  = num_errors
  ROOM_DATA[Room]["client"]["num"]  = num_errors
  ROOM_DATA[Room]["client"]["time"] = knx_time
  FLAT_DATA["client"]["act"]   = all_errors
  FLAT_DATA["client"]["num"]   = all_errors
  FLAT_DATA["client"]["time"]  = tim_errors
  FLAT_DATA["client"]["group"] = ele_errors

  verbose_print (V, "clients online: " + str(all_errors) + " in flat")

  if knx_group in conf_data["Type_Lists"]["blind_door_open"].split(','):
    blinds_auto_away(knx_group)

#########################
#       PERSON		#
#########################
def update_person():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  if knx_group in conf_data['Persons']:
    idx, name = conf_data['Persons'][knx_group].split(':')
    Persons = list(FLAT_DATA['persons']['act'])
    Persons[int(idx)] = name[0] if knx_act == 1 else "-"

    if FLAT_DATA['persons']['act'] != "".join(Persons):
      FLAT_DATA['persons']['act']  = "".join(Persons)
      FLAT_DATA['persons']['time'] = knx_time
      if conf_data['Verbosity']['persons'] == 1: 
        verbose_print(1,FLAT_DATA['persons']['act'])

  else:
    raise Exception(f"{knx_group} in person not OK")

#########################
#     DOOR		#
#########################
def update_door():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['door']

  verbose_print (V, "door: " + knx_group + " knx_act " + str(knx_act))
  if knx_act == -1: raise Exception(f"value -1 for door group {knx_group:s}")
  if (knx_group == '30/7/1'):
    FLAT_DATA["door"]["act"] = 1 - knx_act
    FLAT_DATA["door"]["time"] = time.time()
    verbose_print (V, "door: " + str(FLAT_DATA["door"]["act"]))

#########################
#     LOCK		#
#########################
def update_lock():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['lock']

  FLAT_DATA["lock"]["act"]  = knx_act
  FLAT_DATA["lock"]["time"] = time.time()
  verbose_print (V, "lock: " + str(FLAT_DATA["lock"]["act"]))

  #smart_lock(knx_group, knx_act)

#########################
#     HUMIDITY		#
#########################
def update_humi():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['humi']

  room_humi_array = [0, 3, 4, 5, 6, 7, 10]
  room_bath_rooms = [2, 8, 9]

  knx_act   = knx_act   / 10.0
  knx_alter = knx_alter / 10.0
  Room = ELEM_DATA[knx_group]["room"]

  if Room == conf_data["Debug"]["humi"]:
    knx_act = 85.0
    verbose_print(1,"DEBUG: send wrong humidity to room "+str(Room))

  # room is copied into all rooms except the bath rooms
  # this value is also used for the FLAT
  if Room == 1:
    for i in room_humi_array:
      ROOM_DATA[i]["humi"]["act"] = knx_act
      ROOM_DATA[i]["humi"]["time"] = knx_time
    FLAT_DATA["humi"]["act"] = knx_act
    FLAT_DATA["humi"]["time"] = knx_time

  if Room in [14, 15, 16]:
    ROOM_DATA[Room]["temp"]["act"] = knx_alter
    ROOM_DATA[Room]["temp"]["time"] = knx_time

  if Room == 15:
    ROOM_DATA[17]["humi"]["act"] = knx_act
    ROOM_DATA[17]["humi"]["time"] = knx_time
    ROOM_DATA[17]["temp"]["act"] = knx_alter
    ROOM_DATA[17]["temp"]["time"] = knx_time


  if Room in room_bath_rooms:
    max_humi = 0.0
    max_room = -1
    for i in room_bath_rooms:
      h = ELEM_DATA['8/0/'+str(i)]['act']
      if h > max_humi:
        max_humi = h
        max_room = i
    FLAT_DATA['humi']['maxV'] = max_humi
    FLAT_DATA['humi']['maxE'] = '8/0/'+str(max_room)
    verbose_print (V, f"humidity baths: max in room {max_room:d} at {max_humi:.0f}%")

  ROOM_DATA[Room]["humi"]["act"]  = knx_act
  ROOM_DATA[Room]["humi"]["time"] = knx_time
  FLAT_DATA["humi"]["act"]  = knx_act
  FLAT_DATA["humi"]["time"] = knx_time
  verbose_print (V, "humidity rooms: " + str(knx_act) + "% from " + knx_group + " in room " + str(Room))

#########################
#     BRIGHTNESS        #
#########################
def update_bright():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['bright']

  if (FLAT_DATA["bright"]["act"] > 10000.0) and (knx_act < 10):
    verbose_print(1,"Error in Brightness current {:.0f} to new {:.0f} skipped.".format(FLAT_DATA["bright"]["act"], knx_act))
    return

  verbose_print(V,f"Brightness {knx_act} Lux into flat")
  FLAT_DATA["bright"]["act"]  = knx_act
  FLAT_DATA["bright"]["time"] = knx_time
  verbose_print(V, "Brightness knx_act {:7.0f} to current {:7.0f}".format(knx_act, FLAT_DATA["bright"]["act"]))

#########################
#     FAN		#
#########################
def update_fan():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['fan']

  # toggle if 2
  if ELEM_DATA[knx_group]["act"] == 2:
    ELEM_DATA[knx_group]["act"] = 1 - max(0, min(1, ELEM_DATA[knx_group]["last_act"]))

  # count number of fans running
  # value 0=off // 1=running
  num_fan = 0
  all_fan = 0
  Room  = ELEM_DATA[knx_group]["room"]
  for i_group in ELEM_DATA:
    if ELEM_DATA[i_group]["type"] == "fan":
      all_fan += (ELEM_DATA[i_group]["act"] > 0)
      if ELEM_DATA[i_group]["room"] == Room:
        num_fan += (ELEM_DATA[i_group]["act"] > 0)

  ROOM_DATA[Room]["fan"]["act"]  = num_fan
  ROOM_DATA[Room]["fan"]["time"] = knx_time
  FLAT_DATA["fan"]["act"]  = all_fan
  FLAT_DATA["fan"]["time"] = knx_time

  verbose_print (V, "fan: " + str(num_fan) + " in rooms:" + str(Room))

#########################
#   DAYS FILTER EMPT    #
#########################
def update_dayfil():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['dayfil']

  Days = int(knx_act)
  d = time.time()
  x = datetime.now() + DT.timedelta(days=Days)
  Filter = time.mktime(x.timetuple())

  ELEM_DATA[knx_group]["act"]  = Filter
  ELEM_DATA[knx_group]["time"] = knx_time

  verbose_print (V, f"Filter empty in {Days:d} days.")

#########################
#   DAYS REFILL AQ      '
#########################
def update_dayref():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['dayref']

  d_refill = int(knx_act)

  Days = d_refill // 100
  Hour = d_refill %  100
  if Hour > 24:
    verbose_print(1,"Error: ATO Hour > 24, was {:d}".format(Hour))
    Days += 1
    Hour  = 0

  if Hour == 24: Hour = 23

  d = time.time()
  x = (datetime.now() + DT.timedelta(days=Days)).replace(hour=Hour, minute=0, second=0, microsecond=0)
  refill = time.mktime(x.timetuple())

  p_level = float(knx_alter) / 10.0
  ELEM_DATA['1/2/20']["act"] = p_level
  ELEM_DATA['1/2/20']["time"] = knx_time

  ELEM_DATA[knx_group]["act"] = refill
  ELEM_DATA[knx_group]["time"] = knx_time

  verbose_print(V,"ATO: refill in {:d} days at {:d}:00 now level of {:.1f}cm".format(Days, Hour, p_level))

#########################
#   T AQUARIUM
#########################
def update_t_aqua():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Aquarium']['verbose']

  knx_act = float(knx_act) / 10.0
  ELEM_DATA[knx_group]["act"]  = knx_act

  verbose_print(V,"T_Aq set to {:4.1f}".format(ELEM_DATA[knx_group]["act"]))

#########################
#  Triangle BlueTooth   #
#########################
def update_tri_bt():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, MOBILE
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['tri_bt']

  Ort = ['Light3 Wind', 'Gate Eingang', 'Bad1 Eltern', 'Light5 Arbeit', 'Nord Aquarium']

  code = knx_act // 256
  valu = knx_act %  256
  handy = code // 10

  if not (handy in [1, 2]):
    raise Exception(f"Error: handy {handy} found but only mobile 1+2 are implemented")
  else:
    ort = code %  10
    MOBILE['TRI'][handy][ort] = valu
    MOBILE['TIM'][ort]        = knx_time

  verbose_print(V,f"tri_bt code {code} value {valu} handy {handy} ort {ort}")

  t_old = 0
  i_old = -1
  o_old = -1
  for i in range(5):
    if knx_time - MOBILE['TIM'][i] > t_old:
      t_old = knx_time - MOBILE['TIM'][i]
      o_old = i
  if (t_old > conf_data['General']['tri_max_age'] * 60.0) and (knx_time - software_start_time > 10.0 * 60.0):
    verbose_print(1,f"Achtung TRI Daten fehlen von Ort {o_old:d} {Ort[o_old]:s} seit {t_old/60.0:.1f} Minuten.")

  s_min = 100000
  l_min = 'n/a'
  l_old = ELEM_DATA[knx_group]['pos'+str(handy)]
  for loc in MOBILE['LOC'][handy]:
    s = 0
    for i in range(5): s += (min(24,MOBILE['TRI'][handy][i]) - min(24,MOBILE['LOC'][handy][loc][i]))**2
    if s < s_min:
      s_min = s
      l_min = loc

  if (ELEM_DATA[knx_group]['pos'+str(handy)] != l_min) or (conf_data['Handy'+str(handy)]['verbose'] == 1):

    if s_min < conf_data['Handy'+str(handy)]['err_limit']:
      ELEM_DATA[knx_group]['pos'+str(handy)] = l_min
      ELEM_DATA[knx_group]['time'+str(handy)] = knx_time
      if (MOBILE['TRI'][handy] != [99,99,99,99,99]) and \
        ( (conf_data['Handy'+str(handy)]['verbose'] == 1) or \
          ((conf_data['Handy'+str(handy)]['verbose'] == 2) and (l_min != l_old)) ):
        verbose_print(1,"Triangulation {:1d} {:16s}: {:2d}, {:2d}, {:2d}, {:2d}, {:2d} OK  {:5d}".format( \
          handy, l_min, MOBILE['TRI'][handy][0], MOBILE['TRI'][handy][1], MOBILE['TRI'][handy][2], \
          MOBILE['TRI'][handy][3], MOBILE['TRI'][handy][4], s_min))

    else:
      if ( (MOBILE['TRI'][handy] != [99,99,99,99,99]) or (l_old != "weg")) and \
         ((conf_data['Handy'+str(handy)]['verbose'] == 1) or \
          ((conf_data['Handy'+str(handy)]['verbose'] == 2) and (l_min != l_old)) ):
        verbose_print(1,"Triangulation {:1d} {:16s}: {:2d}, {:2d}, {:2d}, {:2d}, {:2d} ERR {:5d}".format( \
          handy, l_min, MOBILE['TRI'][handy][0], MOBILE['TRI'][handy][1], MOBILE['TRI'][handy][2], \
          MOBILE['TRI'][handy][3], MOBILE['TRI'][handy][4], s_min))

