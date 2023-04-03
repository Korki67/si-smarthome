def write_visu():
# global Xerror
# global FensterCMD
# global BLINDS, LUT_old
# global HEAT_ON, WINDOW_OPEN, SERVER_OFF, CLIENT_ON

  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time
  global visu_file

  knx_act_str = str(knx_act)
  if isinstance(knx_act, float): knx_act_str = f"{knx_act:.1f}"
  if isinstance(knx_act, int  ): knx_act_str = f"{knx_act:d}"

  nobj = open(visu_file + '-tmp', 'w')
  nobj.write('<response>\n')
  nobj.write('<knx_date>' + datetime.now().strftime("%Y.%m.%d %H:%M:%S") + '</knx_date>\n')
  nobj.write(f"<knx_befehl> {knx_group:s} {ELEM_DATA[knx_group]['name']:s} = {knx_act_str:s}</knx_befehl>\n")

#            0       1   2       3                   4    5     6    7       8     9    10
# Adresse    Label   Fg  Type    Koordinaten         Off  Speed mode stamp   %stmp %act idx
  i = 0
  for R in BLINDS:
    if BLINDS[R][0][3] == "a":
      j    = int(BLINDS[R][10])
      nobj.write("<knx_raff" + str(j) + ">"  + \
  	       ELEM_DATA[R]['symbol'] + "," + \
  	       "{:d}%".format(int(BLINDS[R][9]*100.0)) + \
                 "</knx_raff" + str(j) + ">\n")
      i += 1

  Temperatur = {
    "1/3/0" : ["T1", i0, "temperatur" ,"952,400", -99.0],
    "1/3/1" : ["T2", i0, "temperatur" ,"792,360", -99.0],
    "1/3/2" : ["T3", i0, "temperatur" ,"640,416", -99.0],
    "1/3/3" : ["T4", i0, "temperatur" ,"540,416", -99.0],
    "1/3/4" : ["T5", i0, "temperatur" ,"370,428", -99.0],
    "1/3/5" : ["T6", i0, "temperatur" ,"375,272", -99.0],
    "1/3/6" : ["T7", i0, "temperatur" ,"570,189", -99.0],
    "1/3/7" : ["T8", i0, "temperatur" ,"674,264", -99.0],
    "1/3/8" : ["T9", i0, "temperatur" ,"718,206", -99.0]
  }
  
  for L in Temperatur:
    i = int(L.split('/')[2])
    T = ROOM_DATA[i+1]["temp"]["act"]
    nobj.write("<knx_temp" + str(i) + ">" + ELEM_DATA[L]['symbol'] + "," + "{0:.1f}".format(T) + "</knx_temp" + str(i) + ">\n")

  for R in ROOM_DATA:
    nobj.write("<mode_room_" + str(R) + ">" + str(ROOM_DATA[R]["light_mode"]["act"]) + "</mode_room_" + str(R) + ">\n")
    nobj.write("<blind_room_" + str(R) + ">" + str(ROOM_DATA[R]["blind_mode"]["act"])  + "</blind_room_" + str(R) + ">\n")

  i = 0
  pics = ""
  for L in ELEM_DATA:
   if ELEM_DATA[L]['visu'] != '-':
    try:    value = ELEM_DATA[L]["act"]
    except: value = -1
    if conf_data["Debug"]["visu"] == 1: value = 1

    if ((L.split('/')[0] == '20') or (L.split('/')[0] == '30') or (value >= 1)) and (L != "0/0/0"):

      x, y = [int(z) for z in ELEM_DATA[L]['symbol'].split(',')]

      suffix = ".png"
      name   = ELEM_DATA[L]['visu']
      if L.split('/')[0] == '30':
        kate = name.split('_')[0]
        name = name.split('_')[1]
        suffix = "-"
        if kate in ["unity", "server", "switch", "nas", "wlan", "drucker", "cam", "pi"]:
          if value ==  1: suffix = "-"
          if value ==  0: suffix = "#A00000"
          if value == -1: suffix = "#FFA0A0"
          if conf_data["Debug"]["visu"] == 1: suffix = "#A00000"
        else:
          if value ==  1: suffix = "#00A000"
          if value ==  0: suffix = "-"
          if value == -1: suffix = "#A0FFA0"
          if conf_data["Debug"]["visu"] == 1: suffix = "#00A000"
      if name == "temperatur": suffix = "-"
      if name == "raff": suffix = "-"
      if L.split('/')[0] == '20':
        if value ==  1: suffix = "-on.png"
        if value ==  0: suffix = "-off.png"
        if value == -1: suffix = "-off.png"
      if suffix != "-":
        i = i + 1
        nobj.write("<knx_pics" + str(i) + ">" + ELEM_DATA[L]['symbol'] + "," + name + suffix + "</knx_pics" + str(i) + ">\n")

#   if ELEM_DATA[L]["type"] == "window":
#     room = int(L[2:3])+1
#     if 1 <= room <= 9:
#       if ((value == 0) and (Zimmer[room][4] ==  1)) or \
#          ((value == 1) and (Zimmer[room][4] == -1)):
#         i = i + 1
#         x, y = [int(z) for z in ELEM_DATA[L]['symbol'].split(',')]
#         nobj.write("<knx_pics" + str(i) + ">" + str(x+6) + "," + str(y-5) + ",blitz_01.png</knx_pics" + str(i) + ">\n")

# Handy HORST
  if (FLAT_DATA["persons"]['act'][3] == "H") and (conf_data['General']['visu_persons'] == 'yes'):
    if conf_data['Handy1']['set pos'] == "n/a":
      pos = ELEM_DATA['3/0/10']['pos1']
    else:
      pos = conf_data['Handy1']['set pos']
  else:
    pos = "weg"

  if (pos != "weg") or (conf_data['Handy1']['show_absent'] == "yes"):
    i += 1
    nobj.write("<knx_pics" + str(i) + ">" + conf_data['Handy1'][pos] + ",horst_ico2.png</knx_pics" + str(i) + ">\n")

# Handy VIVIANE
  if (FLAT_DATA["persons"]['act'][2] == "V") and (conf_data['General']['visu_persons'] == 'yes'):
    if conf_data['Handy2']['set pos'] == "n/a":
      pos = ELEM_DATA['3/0/10']['pos2']
    else:
      pos = conf_data['Handy2']['set pos']
  else:
    pos = "weg"

  if (pos != "weg") or (conf_data['Handy2']['show_absent'] == "yes"):
    i += 1
    nobj.write("<knx_pics" + str(i) + ">" + conf_data['Handy2'][pos] + ",vivi2.png</knx_pics" + str(i) + ">\n")

  nobj.write('<knx_anzahl>' + str(i) + '</knx_anzahl>\n')

  nobj.write('<speed_ping>' + str(FLAT_DATA["speed"]["PING"]) + '</speed_ping>\n')
  nobj.write('<speed_down>' + str(FLAT_DATA["speed"]["DOWN"]) + '</speed_down>\n')
  nobj.write('<speed_uplo>' + str(FLAT_DATA["speed"]["UPLO"]) + '</speed_uplo>\n')
  nobj.write('<speed_time>' + str(FLAT_DATA["speed"]["time"]) + '</speed_time>\n')

  # Status UV und StroemungsPumpe
  nobj.write('<OZ>' + str(ELEM_DATA['7/0/10']['act'])+ '</OZ>\n')	# Ozon + UV
  nobj.write('<HZ>' + str(ELEM_DATA['7/0/12']['act'])+ '</HZ>\n')	# Heizung
  nobj.write('<SK>' + str(ELEM_DATA['7/0/14']['act'])+ '</SK>\n')	# Skimmer

  # ATO days
  D = ELEM_DATA['1/2/18']['act']
  T = datetime.fromtimestamp(D) - datetime.fromtimestamp(time.time())
  #T = str(T.days) + "d " + datetime.fromtimestamp(D).strftime("%H:00")
  T = str(T.days) + "d"
  nobj.write('<DR>' + T                                  + '</DR>\n')	# days refill

  # ATO height cm
  nobj.write("<DH>{:.1f}cm</DH>\n".format(ELEM_DATA['1/2/20']['act']))	# days refill

  # FILTER
  D = ELEM_DATA['1/2/19']['act']
  T = datetime.fromtimestamp(D) - datetime.fromtimestamp(time.time())
  T = str(T.days) + "d"
  nobj.write('<FI>' + T                                  + '</FI>\n')	# days empty

  # T_Aquarium_Water
  nobj.write(f"<TAQ>{ELEM_DATA['1/2/4']['act']:.1f}</TAQ>\n")

  # Klimaanlagen
  nobj.write('<AC1>' + str(ROOM_DATA[1]['klima']['act'])+ '</AC1>\n')
  nobj.write('<AC6>' + str(ROOM_DATA[6]['klima']['act'])+ '</AC6>\n')

  # Spuelmaschine
  nobj.write('<SPUEL>' + str(ELEM_DATA['7/0/15']['act'])+ '</SPUEL>\n')

  # Room Modes
  mode_txt = {
    0: "0=aus",
    1: "1=alles an",
    2: "2=auto",
    3: "3=essen",
    4: "4=kochen",
    5: "5=relax",
    6: "6=spuelen",
    7: "7=fernsehen"}
  try:    nobj.write('<mode_R1>' + mode_txt[ELEM_DATA['4/3/1']['act']]+ '</mode_R1>\n')
  except: pass

  mode_txt = {
    0: "0=aus",
    1: "1=alles an",
    2: "2=auto",
    3: "3=home office",
    4: "4=n/a",
    5: "5=relax",
    6: "6=n/a",
    7: "7=fernsehen"}
  try:    nobj.write('<mode_R6>' + mode_txt[ELEM_DATA['4/3/6']['act']]+ '</mode_R6>\n')
  except: pass

  # Heizung
  nobj.write(f"<HZ_VOR>{ELEM_DATA['1/2/14']['act']:.1f}</HZ_VOR>\n")
  nobj.write(f"<HZ_RUE>{ELEM_DATA['1/2/15']['act']:.1f}</HZ_RUE>\n")
  nobj.write(f"<HZ_H2O>{ELEM_DATA['1/2/16']['act']:.1f}</HZ_H2O>\n")

  try:    nobj.write('<CO2_R1>' + str(ROOM_DATA[1]['CO2']['act']) + '</CO2_R1>\n')
  except: pass
  try:    nobj.write('<CO2_R5>' + str(ROOM_DATA[5]['CO2']['act']) + '</CO2_R5>\n')
  except: pass
  try:    nobj.write('<CO2_R6>' + str(ROOM_DATA[6]['CO2']['act']) + '</CO2_R6>\n')
  except: pass

  try:    nobj.write('<CO2_C1>' + str(ELEM_DATA['4/7/1']['color']) + '</CO2_C1>\n')
  except: pass
  try:    nobj.write('<CO2_C5>' + str(ELEM_DATA['4/7/5']['color']) + '</CO2_C5>\n')
  except: pass
  try:    nobj.write('<CO2_C6>' + str(ELEM_DATA['4/7/6']['color']) + '</CO2_C6>\n')
  except: pass

  for W in WEATHER:
    nobj.write(f"<{W:s}>{WEATHER[W]}</{W:s}>\n")

  dash_mode = "xml"
  dash_wetter('details')
  for D in DASH_DATA:
    if DASH_DATA[D]['xml']['speak'] != "": nobj.write(f"{DASH_DATA[D]['xml']['speak']}\n")

  nobj.write('</response>\n\n')
  nobj.close()

  out = os.system ("mv {:s}-tmp {:s}".format(visu_file, visu_file))

