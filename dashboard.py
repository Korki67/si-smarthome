# -* coding: utf-8 -*-

dash_vars = ""
dash_olds = ""
dash_mode = "none"
dash_nOKm = 0
dash_save = False

def dash_garage(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm, Garage
  global knx_time

  antwort = ""
  if True:
    dt_max = -1
    G = '9/0/99'
    for G in conf_data['Type_Lists']['garages'].split(','):
      dt = knx_time - ELEM_DATA[G]['time']
      if (dt > dt_max) and (ELEM_DATA[G]['act'] == 0):
        dt_max = dt
        G_max  = G

    level = 4
    action = "none"
    if dt_max >= conf_data["Garagen"]["normal_open"] * 60.0:
      action = ELEM_DATA[G_max]['name'] + " schliessen"
      level = 2
    if dt_max >= conf_data["Garagen"]["longer_open"] * 60.0:
      level = 1
    if dt_max >= conf_data["Garagen"]["extrem_open"] * 60.0:
      level = 0

    reason = "open" if level != 4 else "none"
    element_alarm('1/2/9', 9, level, reason, action)

    if dash_mode == "speak":

      if G_max == '9/0/99': antwort = antwort + "Alle Garagen sind geschlossen. "
      else:
        antwort = antwort + ELEM_DATA[G_max]['name'] + " ist "
        if level == 0: antwort = antwort + "sehr lange auf. "
        if level == 1: antwort = antwort + "etwas länger auf. "
        if level == 2: antwort = antwort + "gerade geöffnet worden. "

      if (Object == "garage") or (Object == "garagen") or (Object == "details"):
        antwort = antwort + "Im Detail: "

        for G in conf_data['Type_Lists']['garages'].split(','):
          antwort += ELEM_DATA[G]['name'] + " "
          if   ELEM_DATA[G]['act'] == 0: antwort += "auf seit "
          elif ELEM_DATA[G]['act'] == 1: antwort += "zu seit "
          else: antwort += "keine Info seit "
          antwort += duration(knx_time-ELEM_DATA[G]['time']) + ". "

    else:
      if level == 4: antwort += dash_out_xml("garage", "Garagen", "OK")
      else:
        dash_nOKm = dash_nOKm + 1
        garage = "Offen: " if level > 2 else "ALARM: "
        garage += ELEM_DATA[G_max]['name'].replace('Garage ','')
        antwort = antwort + dash_out_xml("garage", "Garagen", garage)

  if False:
    if dash_mode == "speak":
      antwort = "Fehler bei der Auswertung der Garagen. "
    else:
      antwort = antwort + dash_out_xml("garage", "Garagen", "Fehler")

  DASH_DATA["garage"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  return antwort

def dash_bright(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm

  antwort = dash_out_xml("bright", "Brightnes", f"{ELEM_DATA['1/5/1']['act']}")
  DASH_DATA["bright"]['xml'] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  return antwort

def dash_CO2(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm

  antwort = ""
  level_min = 4
  E_ok = []
  E_ye = []
  E_re = []
  for E in conf_data['Type_Lists']['CO2'].split(','):
    reason = "none"
    action = "none"
    level  = 4
    room = ELEM_DATA[E]["room"]
    CO2_act = ELEM_DATA[E]["act"]
    CO2_flg = ELEM_DATA[E]["flag"]
    try:
      d_y = conf_data['Room'+str(room)]['delay_y']
      d_r = conf_data['Room'+str(room)]['delay_r']
    except:
      d_y = conf_data['CO2']['delay_y']
      d_r = conf_data['CO2']['delay_r']

    if CO2_flg != "green":
      reason = "high"
      action = "open"
      level  = 3 if CO2_flg == "yellow" else 2
      level_min = min(level, level_min)
    
    element_alarm(E, 9, level, reason, action)

    if   CO2_flg == "red":    E_re.append(E)
    elif CO2_flg == "yellow": E_ye.append(E)
    else:                     E_ok.append(E)

  if dash_mode == "speak":
    if level_min == 4:
      antwort += "Kohlendioxid überall OK. "

    else:
      dash_nOKm = dash_nOKm + 1
      E_check = []
      E_check.extend(E_ye)
      E_check.extend(E_re)
      rooms_ok = ""
      for E in E_ok: rooms_ok += ROOM_DATA[ELEM_DATA[E]["room"]]['name'] + ", "
      if len(E_ok) > 1: rooms_ok = ' und'.join(rooms_ok[:-2].rsplit(',', 1)) + ". "
      else:             rooms_ok = rooms_ok[:-2] + ". "
      rooms_check = ""
      for E in E_check: rooms_check += ROOM_DATA[ELEM_DATA[E]["room"]]['name'] + ", "
      if len(E_check) > 1: rooms_check = ' und'.join(rooms_check[:-2].rsplit(',', 1)) + ". "
      else:                rooms_check = rooms_check[:-2] + ". "

      if len(E_ok) != 0: antwort += "Kohlendioxid OK in " + rooms_ok
      antwort += "Kohlendioxid zu hoch in " + rooms_check

    if Object in ["kohlendioxid", "details"]:
      antwort += "Im Detail: "
      for E in conf_data['Type_Lists']['CO2'].split(','):
        raum = ROOM_DATA[ELEM_DATA[E]["room"]]['name']
        CO2  = 100 * int((ELEM_DATA[E]["act"]+50)/100)
        antwort += "{:s} {:d}, ".format(raum, CO2)
      antwort = antwort[:len(antwort)-2]
      antwort = ' und'.join(antwort.rsplit(',', 1)) + " ppm. "

  if dash_mode == "xml":
    if level_min == 4:
      antwort = antwort + dash_out_xml("co2", "CO2", "OK")
    else:
      dash_nOKm = dash_nOKm + 1
      E_check = []
      E_check.extend(E_ye)
      E_check.extend(E_re)
      rooms = ""
      if len(E_check) > 0:
        for E in E_check:
          rooms += ROOM_DATA[ELEM_DATA[E]["room"]]['name'] + ", "
        if len(E_check) > 1: rooms = ' und'.join(rooms.rsplit(',', 1))
      else:
        if time.time()-software_start_time > 5.0*60:
          verbose_print(1,"Error in CO2: level_min != 4 but nothing to check.")

      CO2 = "CO2 hoch. Bitte {:s} lüften. ".format(rooms)
      antwort = antwort + dash_out_xml("co2", "CO2", CO2)

  DASH_DATA["CO2"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  return antwort

def dash_dayref(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm, Garage

  antwort = ""
  if True:
    ELEM_DATA['1/2/18']['act'] = int(ELEM_DATA['1/2/18']['act'])
  if False:
    ELEM_DATA['1/2/18']['act'] = 102

  D = ELEM_DATA['1/2/18']['act']
  T = datetime.fromtimestamp(D) - datetime.fromtimestamp(time.time())

  days = T.days
  hour = datetime.fromtimestamp(D).hour

  level   = 4
  action  = "none"
  reason  = "none"
  flag    = "OK"
  antwort = "Nachfüllanlage hält mehr als {:d} Tage. ".format(days)

  if days < 3:
    level = 3
    flag  = "2 Tage"
    action = "refill"
    reason = "leer"
    antwort = "Osmosewasser übermorgen leer. Bitte bald nachfüllen. ".format(days)

  if days < 2:
    level = 2
    flag  = "1 Tag"
    action = "refill"
    reason = "leer"
    antwort = "Osmosewasser morgen gegen {:d} Uhr leer. Bitte heute nachfüllen. ".format(hour)

  if days < 1:
    level = 1
    flag  = "{:d} Stunden".format(hour)
    action = "refill"
    reason = "leer"
    antwort = "Osmosewasser heute gegen {:d} Uhr leer. Bitte jetzt nachfüllen. ".format(hour)

  reason = "refill" if level != 4 else "none"
  element_alarm('1/2/18', 2, level, reason, action)

  if dash_mode == "xml":
    antwort = dash_out_xml("dayref", "DAYREF", f"{days:.1f}")

  DASH_DATA["dayref"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  return level, flag, action, reason, antwort

def dash_dayfil(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm, Garage

  antwort = ""
  days = (ELEM_DATA['1/2/19']['act'] - time.time()) / 60.0 / 60.0 / 24.0

  level   = 4
  action  = "none"
  reason  = "none"
  flag    = "OK"
  antwort = "Filterpapier ausreichend für mehr als 2 Wochen. "

  if days <= 14:
    level = 3
    flag  = "bald leer"
    action = "prepare"
    reason = "short"
    categ  = "ALERT"
    antwort = "Papierrolle in ca. {:.0f} Tagen leer. ".format(days)

  if days <= 7:
    level = 2
    flag  = "bald leer"
    action = "prepare"
    categ  = "ALERT"
    reason = "short"
    antwort = "Papierrolle in Kuerze leer. Prognose nicht möglich. "

  if days <= 14:
    if True:
      if time.time() - ELEM_DATA['1/2/19']['mail'] > 24.0*60.0*60.0:
        info_system_mail(categ, antwort, '/home/pi/eHome/aquarium.txt')
        ELEM_DATA['1/2/19']['mail'] = time.time()
    if False: 
      info_system_mail(categ, antwort.replace('ä', 'ae'), '/home/pi/eHome/papierrolle.txt')
      ELEM_DATA['1/2/19']['mail'] = time.time()

  alarm = copy.deepcopy(ALARM_OBJ)
  alarm["prio"] = 2
  alarm["time"] = time.time()
  alarm["type"] = ELEM_DATA['1/2/19']["type"]
  alarm["level"] = level
  alarm["reason"] = "refill" if level != 4 else "none"
  alarm["action"] = action
  alarm["group"] = '1/2/19'
  element_alarm(alarm['group'],alarm['prio'],alarm['level'],alarm['reason'],alarm['action'])

  if dash_mode == "xml":
    antwort = dash_out_xml("dayfil", "DAYFIL", f"{days:.1f}")

  DASH_DATA["dayfil"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  return level, flag, action, reason, antwort

def dash_beauf(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm

  antwort = ""
  level = 4
  windSPDave = float(FLAT_DATA['beauf']["speed_av"])
  windBFTave = float(FLAT_DATA['beauf']["beauf_av"])
  windSPDmax = float(FLAT_DATA['beauf']["speed_mx"])
  windBFTmax = float(FLAT_DATA['beauf']["beauf_mx"])

  if dash_mode == "speak":
    if   (windBFTave < 0.01                               ) and (windBFTmax < 0.01                               ):
      antwort = antwort + "Es ist windstill.          "
    elif (windBFTave < conf_data["Wind"]["weaker_BFT_ave"]) and (windBFTmax < conf_data["Wind"]["weaker_BFT_max"]):
      antwort = antwort + "Der Wind ist sehr schwach. "
    elif (windBFTave < conf_data["Wind"]["normal_BFT_ave"]) and (windBFTmax < conf_data["Wind"]["normal_BFT_max"]):
      antwort = antwort + "Der Wind ist moderat. "
    elif (windBFTave < conf_data["Wind"]["strong_BFT_ave"]) and (windBFTmax < conf_data["Wind"]["strong_BFT_max"]):
      antwort = antwort + "Der Wind ist etwas stärker. "
    elif (windBFTave < conf_data["Wind"]["extrem_BFT_ave"]) and (windBFTmax < conf_data["Wind"]["extrem_BFT_max"]):
      antwort = antwort + "Der Sturm ist stark. "
      dash_nOKm = dash_nOKm + 1
      level = 3
    else:
      antwort = antwort + "Der Sturm ist extrem stark. "
      dash_nOKm = dash_nOKm + 1
      level = 0

    if ((Object == "wind") or (Object == "details")) and (windBFTave > 0.01):
      wind = "Windstärke im Mittel %.1f mit Spitzen von %.0f Beaufort. " % (windBFTave, windBFTmax)
      antwort = antwort + wind.replace('.', ',', 1)
      wind = "Windgeschwindigkeit im Mittel %.1f mit Spitzen von %.0f kmh. " % (windSPDave, windSPDmax)
      antwort = antwort + wind.replace('.', ',', 1)

  else:
    if   (windBFTave < conf_data["Wind"]["weaker_BFT_ave"]) and (windBFTmax < conf_data["Wind"]["weaker_BFT_max"]):
      antwort = antwort + dash_out_xml("wind", "Wind", "OK %.1f Bf" % (windBFTmax))
    elif (windBFTave < conf_data["Wind"]["normal_BFT_ave"]) and (windBFTmax < conf_data["Wind"]["normal_BFT_max"]):
      antwort = antwort + dash_out_xml("wind", "Wind", "OK %.1f Bf" % (windBFTmax))
    elif (windBFTave < conf_data["Wind"]["strong_BFT_ave"]) and (windBFTmax < conf_data["Wind"]["strong_BFT_max"]):
      antwort = antwort + dash_out_xml("wind", "Wind", "Info: %.1f Bf" % (windBFTmax))
    elif (windBFTave < conf_data["Wind"]["extrem_BFT_ave"]) and (windBFTmax < conf_data["Wind"]["extrem_BFT_max"]):
      antwort = antwort + dash_out_xml("wind", "Wind", "ALERT: %.1f Bf" % (windBFTmax))
      dash_nOKm = dash_nOKm + 1
      level = 3
    else:
      antwort = antwort + dash_out_xml("wind", "Wind", "ALERT: %.1f Bf" % (windBFTmax))
      dash_nOKm = dash_nOKm + 1
      level = 0

    amb_press = ELEM_DATA['8/0/20']['act']
    antwort += dash_out_xml("windSPDave", "Wind km/h ave", f"{windSPDave:.1f}")
    antwort += dash_out_xml("windSPDmax", "Wind km/h max", f"{windSPDmax:.1f}")
    antwort += dash_out_xml("windBFTave", "Wind Bft ave",  f"{windBFTave:.1f}")
    antwort += dash_out_xml("windBFTmax", "Wind Bft max",  f"{windBFTmax:.1f}")
    antwort += dash_out_xml("amb-press",  "Ambient press", f"{amb_press:.0f}")

  element_alarm('1/2/6', 1, level, 'storm', 'protect')

  DASH_DATA["beauf"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  return antwort

def zimmer_xml(i):
  return ""
  global Zimmer

  Zimmer[1+i][5] = round(Zimmer[1+i][5])
  out = ""
  out = out + "<dash_zimmer_"+str(1+i)+"_Name>" +                  Zimmer[1+i][0]  + "</dash_zimmer_"+str(1+i)+"_Name>\n"
  out = out + "<dash_zimmer_"+str(1+i)+"_Temp>" + '{:5.1f}'.format(Zimmer[1+i][1]) + "</dash_zimmer_"+str(1+i)+"_Temp>\n"
  out = out + "<dash_zimmer_"+str(1+i)+"_Humi>" + '{:5.0f}'.format(Zimmer[1+i][2]) + "</dash_zimmer_"+str(1+i)+"_Humi>\n"
  out = out + "<dash_zimmer_"+str(1+i)+"_Stat>" + '{:5.0f}'.format(Zimmer[1+i][3]) + "</dash_zimmer_"+str(1+i)+"_Stat>\n"
  out = out + "<dash_zimmer_"+str(1+i)+"_Flag>" + str(Zimmer[1+i][4]) + "</dash_zimmer_"+str(1+i)+"_Flag>\n"
  out = out + "<dash_zimmer_"+str(1+i)+"_Raff>" + '{:5.0f}'.format(Zimmer[1+i][5]) + "</dash_zimmer_"+str(1+i)+"_Raff>\n"

  return out

def dash_zimmer(Object):
  return ""

  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm
  global Zimmer, Windows

  antwort = ""
  humi_all = ROOM_DATA[1]["humi"]["act"]
  humi_bd1 = ROOM_DATA[8]["humi"]["act"]
  humi_bd2 = ROOM_DATA[9]["humi"]["act"]
  humi_bd3 = ROOM_DATA[2]["humi"]["act"]

  win_status = -1	# -1 undef // 0=alle zu // 1=min 1 auf
  win_flag   =  0	# -1 zu kalt // 0 OK // 1 zu warm
  jalou      = -1	# -1 undef Status Jalousie(en)
  undef      = -1	# -1 undef Status Licht

  # -----------------------
  #    FAN BAD2
  # -----------------------
  fan2         = '0/3/19'
  hyst         = conf_data["Room9"]["fan_hyst"]
  humi_limit   = conf_data["Room9"]["fan_humi"]
  humi_delta   = conf_data["Room9"]["fan_delta"]
  fan_duration = conf_data["Room9"]["fan_duration"]

  if (ELEM_DATA[fan2]["act"] < 1) and \
     (time.time() > ELEM_DATA[fan2]["time"]+fan_duration*60.) and \
     (humi_bd2 > min(humi_limit, humi_all+humi_delta) + hyst):
    os.system('./eib '+fan2+' 1 > /dev/null &')
    verbose_print(1,"Info: fan in bad2 switched ON as humidity is high.")

  if (ELEM_DATA[fan2]["act"] == 1) and \
     (time.time() > ELEM_DATA[fan2]["time"]+fan_duration*60.) and \
     (humi_bd2 < min(humi_limit, humi_all+humi_delta) - hyst):
    os.system('./eib '+fan2+' 0 > /dev/null &')
    verbose_print(1,"Info: switched fan in bad2 OFF due to timing.")

  # -----------------------
  #  ANALYSE ZIMMER
  # -----------------------
  Zimmer = { # 0          1                            2         3           4         5      6
    1	: ["Wohn Süd",   ROOM_DATA[1]["temp"]["act"], humi_all, win_status, win_flag, jalou, undef],
    2	: ["Bad Kinder", ROOM_DATA[2]["temp"]["act"], humi_bd3, win_status, win_flag, jalou, undef],
    3	: ["Fiona",      ROOM_DATA[3]["temp"]["act"], humi_all, win_status, win_flag, jalou, undef],
    4	: ["Delia",      ROOM_DATA[4]["temp"]["act"], humi_all, win_status, win_flag, jalou, undef],
    5	: ["Arbeit",     ROOM_DATA[5]["temp"]["act"], humi_all, win_status, win_flag, jalou, undef],
    6	: ["Wohn Nord",  ROOM_DATA[6]["temp"]["act"], humi_all, win_status, win_flag, jalou, undef],
    7	: ["Eltern",     ROOM_DATA[7]["temp"]["act"], humi_all, win_status, win_flag, jalou, undef],
    8	: ["Bad Eltern", ROOM_DATA[8]["temp"]["act"], humi_bd1, win_status, win_flag, jalou, undef],
    9	: ["Gäste WC",   ROOM_DATA[9]["temp"]["act"], humi_bd2, win_status, win_flag, jalou, undef]
  }

  # insert blinds
  for i in range(9): Zimmer[i+1][5] = ROOM_DATA[i+1]["blinds"]["av"]

  if True: Temp_aussen = float(WEATHER["w_T_outside"])
  if False:
    Temp_aussen = 16.0
    verbose_print(1,"ERROR - no T_aussen found. check weather data.")
  Flag_ges = 0
  T_min =  99.0
  T_max = -99.0
  i_min = -1
  i_max = -1
  act_time = time.time()
  sun_time = datetime.now()

  for i in range(9):
    reason = "none"
    action = "none"

    # Anzahl offener Fenster lesen (0=alle zu)
    Zimmer[i+1][3] = ROOM_DATA[i+1]["window"]["no"]

    # if Temp = -99.0 initial value => Annahme  20.0
    if Zimmer[i+1][1] < -90.0: Zimmer[i+1][1] = 20.0

    # find room with lowest temperature
    if (T_min > Zimmer[i+1][1]):
      T_min = min(T_min, Zimmer[i+1][1])
      i_min = i+1

    # find room with highest temperature
    if (T_max < Zimmer[i+1][1]):
      T_max = max(T_max, Zimmer[i+1][1])
      i_max = i+1

    # wanted temperature
    if True:    T_0 = conf_data["Room"+str(i+1)]["temp_standard"]
    if False: T_0 = conf_data["Zimmer"]["temp_standard"]

    # Ermittle waermen oder kuehlen             # 0=angenehm 1=heizen -1=kuehlen
    Sign = 0.0					# Raum angenehm => OK
    DC = conf_data["Zimmer"]["delta_cool"]
    DH = conf_data["Zimmer"]["delta_heat"]
    if T_0-DH >= Zimmer[i+1][1]:
      Sign =  1					# Raum zu kalt  => heizen
      reason = "cold"
    if T_0+DC <= Zimmer[i+1][1]:
      Sign = -1					# Raum zu warm  => kuehlen
      reason = "hot"
    if i+1 == 7:
      if T_0-10.0 < Zimmer[i+1][1]:
        Sign =  0   				# Eltern kuehler
        reason = "none"

    # Kennzahl / Flag -1=ZU  0=OK  1=AUF
    Kenn = (Temp_aussen-Zimmer[i+1][1])*Sign	# D_T>0 rein, D_T<0 raus
    Flag = 0					# Flag  0 = Fenster EGAL
    DW = conf_data["Zimmer"]["delta_outer"]
    if Kenn < -DW: Flag = -1			# Flag -1 = Fenster soll zu
    if Kenn >  DW: Flag =  1			# Flag +1 = Fenster soll auf

    # Fenster zu falls Raum angenehm (Flag == 0)
    if (abs(Temp_aussen - Zimmer[i+1][1]) > DW) and (Sign == 0):
      if i+1 != 7:
        Flag = -1				# Fenster schliessen
        reason = "OK"
  
    # pruefe mit Feuchtigkeit
    # Zimmer 0=nix 1=wait 2=ALARM
    humi = Zimmer[i+1][2]
    humi_max = conf_data["Zimmer"]["humi_max"]
    if (humi > humi_max) and (Zimmer[i+1][3] > 0):
      Zimmer[i+1][4] = 2			# 2=wait
      reason = "humid"
      action = "wait"
    else:
      if humi > humi_max:
        Zimmer[i+1][4] = 1			# aufmachen weil zu feucht
        reason = "humid"
        action = "open"
      else:
        Zimmer[i+1][4] = Flag
        if Flag ==  1: action = "open"
        if Flag == -1:
          action = "close"
          if reason == "none": reason = "OK"

    # Abgleich mit Status fuer Handlung
    # tu nichts falls -1=-1 oder 1=1
    if (Zimmer[i+1][3]>0)*2-1 == Zimmer[i+1][4]:
      Zimmer[i+1][4] = 0
      if (Sign != 0) and (Zimmer[i+1][4] == 1): Zimmer[i+1][4] = 2

    # Nix fuer Gaeste-WC mit Luefter
    if i+1 == 9:
      Zimmer[i+1][4] = 0			  # Gaeste WC Luefter
      Zimmer[i+1][3] = ROOM_DATA[9]["fan"]["act"] # Status Luefter

    # -----------------------
    #  CHECK SLEEP WINDOW OPEN
    # -----------------------
    if True:
      MediaOK = check_time("4/3/"+str(i+1), "window_sleep")
      if MediaOK:
        Zimmer[i+1][4] = 0
        reason = "OK"
        action = "close"
    if False:
      pass

    # gesamt-Flag: 0=OK // 1=wait // 2=ALARM
    if (abs(Zimmer[i+1][4]) == 1): Flag_ges = 2
    if (Zimmer[i+1][4] == 2):      Flag_ges = max(Flag_ges, 1)

    # -----------------------
    #  ANALYSE WINDOWS
    # -----------------------
    Alarm = copy.deepcopy(ALARM_OBJ)
    Alarm["level"] = 4 - 2*(abs(Zimmer[i+1][4]) == 1)
    if Alarm["level"] == 4:
      reason = "none"
      action = "none"
    Alarm["prio"] = 10
    Alarm["time"] = act_time
    Alarm["type"] = "window"
    Alarm["reason"] = reason
    Alarm["action"] = action

    verbose_print(5,"Dash Window room {:d} reason {:s} action {:s} level {:d}".format(i+1, reason, action, Alarm["level"]))

    if ROOM_DATA[i+1]["temp"]["act"] < 0.0:
      Alarm["level"] = 4
      Alarm["reason"] = "none"
      Alarm["action"] = "none"
    if (reason == "none") and (action != "none"):
      verbose_print(1,"reason none: Sign " + str(Sign) + " Flag " + str(Flag) + " room " + str(i+1))
    if len(Windows[i+1]) > 0:
      for E in Windows[i+1]:
        Alarm["group"] = E
        element_alarm(alarm['group'],alarm['prio'],alarm['level'],alarm['reason'],alarm['action'])
        verbose_print(5,"  applied to " + E)
    else:
      verbose_print(5,"  no window found.")

    # -----------------------
    #  ANALYSE BLINDS in room
    # -----------------------
    for B in Blinds[i+1]:
      Alarm = copy.deepcopy(ALARM_OBJ)
      Alarm["prio"] = 11
      Alarm["time"] = act_time
      Alarm["type"] = "blinds"
      case, p = calc_blind_angle(B, sun_time, 5)
      adjust = (Zimmer[i+1][1] > T_0 + 3.0) and (case == 2) and (BLINDS[B][9] - p > conf_data["BLINDS"]["warn_adjust"])
      #if (BLINDS[B][1] < time.time()) and (B in RAFF_KEYS) and (case == 2):
      #  BLINDS[B][10] = BLINDS[B][9] - p
      #else:
      #  BLINDS[B][10] = -1

      Alarm["level"] = 4 - 2*adjust
      Alarm["reason"] = "none" if not adjust else "hot"
      Alarm["action"] = "none" if not adjust else "lower"
      Alarm["group"] = B
      element_alarm(alarm['group'],alarm['prio'],alarm['level'],alarm['reason'],alarm['action'])

  if Flag_ges > 0: dash_nOKm = dash_nOKm + 1
  if True:
    if dash_mode == "speak":
      room_list = []
      for i in range(9):
         if Zimmer[i+1][4] != 0: room_list.append(Zimmer[i+1][0])

      num = len(room_list)
      if num > 0: rooms = ', '.join(room_list)
      else:       rooms = ""
      if num > 1: rooms = ' und'.join(rooms.rsplit(',', 1))

      if Flag_ges == 0: antwort = antwort + "Alle Zimmer in Ordnung. "
      if Flag_ges == 1: antwort = antwort + "Bei den Zimmern gibt es eine Info. Bitte nachsehen in " + rooms + ". "
      if Flag_ges == 2:
        if num > 1: antwort = antwort + "Bei den Zimmern gibt es Probleme: Bitte nachsehen in " + rooms + ". "
        else:       antwort = antwort + "Bei den Zimmern gibt es ein Problem: Bitte nachsehen in " + rooms + ". "
      if (Object == "zimmer") or (Object == "details"):
        antwort = antwort + "Niedrigste Temperatur in " + Zimmer[i_min][0] + " {:.0f} Grad".format(T_min) + ". "
        antwort = antwort + "Höchste Temperatur in " + Zimmer[i_max][0] + " {:.0f} Grad Celsius".format(T_max) + ". "
        antwort = antwort + "Feuchtigkeiten: Küche {:.0f}, Bad Eltern {:.0f}, Kinder {:.0f}, Gäste {:.0f} Prozent. ".format(humi_all, humi_bd1, humi_bd3, humi_bd2)

        liste = []
        for R in ROOM_DATA:
          if ROOM_DATA[R]["light"]["no"] > 0:
            liste.append(ROOM_DATA[R]["name"])
        if len(liste) == 0:
          antwort = antwort + "Alle Lampen in der Wohnung sind aus. "
        else:
          licht = ', '.join(liste)
          licht = ' und'.join(licht.rsplit(',', 1))
          if len(liste) == 1:
            antwort = antwort + "In " + licht + "ist das Licht an. "
          else:
            antwort = antwort + "In diesen Räumen ist Licht an: " + licht + ". "

        door = FLAT_DATA["door"]["act"]
        lock = FLAT_DATA["lock"]["act"]

        level = 4
        if (door == 1) and (time.time() - FLAT_DATA["door"]["time"] > conf_data["Alarm"]["door_open_info"] * 60.0):
          level = 3
        if (door == 1) and (time.time() - FLAT_DATA["door"]["time"] > conf_data["Alarm"]["door_open_warn"] * 60.0):
          level = 0
        alarm = copy.deepcopy(ALARM_OBJ)
        alarm["prio"]   = 4
        alarm["time"]   = time.time()
        alarm["type"]   = "door"
        alarm["level"]  = level
        alarm["reason"] = "open"  if level != 4 else "none"
        alarm["action"] = "close" if level != 4 else "none"
        alarm["group"]  = '30/7/2'
        element_alarm(alarm['group'],alarm['prio'],alarm['level'],alarm['reason'],alarm['action'])
      
        antwort = antwort + "Die Wohnungstür ist "
        if door == 0:
          antwort = antwort + "zu seit "                  + duration(time.time()-FLAT_DATA["door"]["time"])
        else:
          antwort = antwort + "auf seit "                 + duration(time.time()-FLAT_DATA["door"]["time"])
        antwort = antwort + ". "
        antwort = antwort + "Der Türriegel ist "
        if   lock == 0:
          antwort = antwort + "offen seit "               + duration(time.time()-FLAT_DATA["lock"]["time"])
        elif lock == 1:
          antwort = antwort + "in Zwischenstellung seit " + duration(time.time()-FLAT_DATA["lock"]["time"])
        elif lock == 2:
          antwort = antwort + "geschlossen seit "         + duration(time.time()-FLAT_DATA["lock"]["time"])
        else:
          antwort = antwort + "nicht bekannt"
        antwort = antwort + ". "

    else:
      for i in range(9):
        antwort = antwort + zimmer_xml(i)

      if Flag_ges == 0: antwort = antwort + dash_out_xml("zimmer", "Zimmer", "OK")
      if Flag_ges == 1: antwort = antwort + dash_out_xml("zimmer", "Zimmer", "Info: wait")
      if Flag_ges == 2: antwort = antwort + dash_out_xml("zimmer", "Zimmer", "Info: act")

  if False:
    if dash_mode == "speak":
      antwort = "Fehler bei der Auswertung der Zimmer. "
    else:
      antwort = antwort + dash_out_xml("zimmer", "Zimmer", "Fehler")

  DASH_DATA["zimmer"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  return antwort

def dash_waschmaschine(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm, Blinds

  antwort = ""
  prio   = 0
  level  = 4
  reason = "none"
  action = "none"
  if dash_mode == "speak":
    alarm_txt = "Wassersensor Waschmaschine ist OK. "
    if (Object == "Waschmaschine") or (Object == "details"):
      dauer  = duration(time.time() - ELEM_DATA['4/0/9']["time"])
      alarm_txt = alarm_txt + "Letztes Signal vom Wassersensor Waschmaschine vor {:s} erhalten. ".format(dauer)
    if ELEM_DATA['4/0/9']["time"] < time.time() - 10.0*60.0:
      prio   = 3
      level  = 0
      reason = "not_alive"
      action = "check"
      dauer  = duration(time.time() - ELEM_DATA['4/0/9']["time"])
      alarm_txt = "Letztes Signal vom Wassersensor Waschmaschine vor {:s} erhalten. Bitte prüfen. ".format(dauer)
    if ELEM_DATA['4/0/9']["act"] == 0:
      prio   = 0
      level  = 0
      reason = "water"
      action = "check"
      alarm_txt = "Der Wassersensor Waschmaschine sieht Wasser. Bitte sofort prüfen. "
  else:
    alarm_txt = dash_out_xml("wasser_sensor", "Wassersensor", "OK")
 
  alarm  = copy.deepcopy(ALARM_OBJ)
  alarm["prio"]   = prio
  alarm["time"]   = time.time()
  alarm["type"]   = "water"
  alarm["level"]  = level
  alarm["reason"] = reason
  alarm["action"] = action
  alarm["group"]  = '4/0/9'
  element_alarm(alarm['group'],alarm['prio'],alarm['level'],alarm['reason'],alarm['action'])

  antwort = antwort + alarm_txt

  if level < 4: dash_nOKm = dash_nOKm + 1

  return antwort

def dash_wasseraquarium(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm, Blinds

  antwort = ""
  prio   = 0
  level  = 4
  reason = "none"
  action = "none"
  flag   = "OK"
  
  if dash_mode == "speak":
    alarm_txt = "Wassersensor Aquarium ist OK. "
    if (Object == "aquarium") or (Object == "details"):
      dauer  = duration(time.time() - ELEM_DATA['4/0/11']["time"])
      alarm_txt = alarm_txt + "Letztes Signal vom Wassersensor Aquarium vor {:s} erhalten. ".format(dauer)
    if ELEM_DATA['4/0/11']["time"] < time.time() - 2.0*60.0:
      prio   = 3
      level  = 0
      reason = "not_alive"
      action = "check"
      dauer  = duration(time.time() - ELEM_DATA['4/0/11']["time"])
      alarm_txt = "Letztes Signal vom Wassersensor Aquarium vor {:s} erhalten. Bitte prüfen. ".format(dauer)
    if ELEM_DATA['4/0/11']["act"] == 0:
      prio   = 0
      level  = 0
      reason = "water"
      action = "check"
      alarm_txt = "Der Wassersensor Aquarium sieht Wasser. Bitte sofort prüfen. "
  else:
    alarm_txt = dash_out_xml("aquarium_sensor", "Wassersensor", "OK")
 
  alarm  = copy.deepcopy(ALARM_OBJ)
  alarm["prio"]   = prio
  alarm["time"]   = time.time()
  alarm["type"]   = "water"
  alarm["level"]  = level
  alarm["reason"] = reason
  alarm["action"] = action
  alarm['group']  = '4/0/11'
  element_alarm(alarm['group'],alarm['prio'],alarm['level'],alarm['reason'],alarm['action'])

  antwort = antwort + alarm_txt

  return level, flag, action, reason, antwort

def dash_water(Object):
  global knx_group

  antwort  = dash_wasseraquarium(Object)
  antwort += dash_waschmaschine(Object)

  DASH_DATA["water"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  return antwort

def dash_t_aqua(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm, Blinds

  antwort = ""
  prio   = 0
  level  = 4
  reason = "none"
  action = "none"
  flag   = "OK"

  temp = ELEM_DATA['1/2/4']['act']
  antwort = "Wasser ist mit {:.1f} Grad Celsius perfekt. ".format(temp)

  if temp > conf_data['Aquarium']['aq_heat_off_at']+0.2:
    antwort = "Das Wasser ist mit {:.1f} Grad Celsius etwas zu warm. ".format(temp)
    level   = 3
    action  = "cool"
    reason  = "warm"
    flag    = "kuehlen"
  
  if temp > conf_data['Aquarium']['aq_heat_off_at']+1.5:
    antwort = "Das Wasser ist mit {:.1f} Grad Celsius zu warm. ".format(temp)
    level   = 2
    action  = "cool"
    reason  = "warm"
    flag    = "kuehlen"
  
  if temp > conf_data['Aquarium']['aq_heat_off_at']+3.0:
    antwort = "Das Wasser ist mit {:.1f} Grad Celsius viel zu warm. ".format(temp)
    level   = 1
    action  = "cool"
    reason  = "warm"
    flag    = "kuehlen"
  
  if temp < conf_data['Aquarium']['aq_heat_on_at']-0.5:
    antwort = "Das Wasser ist mit {:.1f} Grad Celsius etwas zu kalt. ".format(temp)
    level   = 3
    action  = "heat"
    reason  = "cool"
    flag    = "heizen"
  
  if temp < conf_data['Aquarium']['aq_heat_on_at']-2.0:
    antwort = "Das Wasser ist mit {:.1f} Grad Celsius zu kalt. ".format(temp)
    level   = 2
    action  = "heat"
    reason  = "cool"
    flag    = "heizen"
  
  if temp < conf_data['Aquarium']['aq_heat_on_at']-4.0:
    antwort = "Das Wasser ist mit {:.1f} Grad Celsius viel zu kalt. "
    level   = 1
    action  = "heat"
    reason  = "cool"
    flag    = "heizen"

  HEIZ = "an" if ELEM_DATA['7/0/12']['act'] == 1 else "aus"
  ABSC = "an" if ELEM_DATA['7/0/14']['act'] == 1 else "aus"
  UVOZ = "an" if ELEM_DATA['7/0/10']['act'] == 1 else "aus"

  AN = ""
  if HEIZ == "an": AN += "Heizung, "
  if ABSC == "an": AN += "Abschäumer, "
  if UVOZ == "an": AN += "UV, Ozon, "
  if True: AN = AN.rsplit(',',1)[0] + " "
  if False: pass

  f = AN.count(',')
  if   f > 1:
    AN = ' und'.join(AN.rsplit(',', 1))
    antwort += AN + "sind eingeschaltet. "
  elif f == 1:
    AN = ' und'.join(AN.rsplit(',', 1))
    antwort += AN + "ist eingeschaltet. "

  AUS = ""
  if HEIZ == "aus": AUS += "Heizung, "
  if ABSC == "aus": AUS += "Abschäumer, "
  if UVOZ == "aus": AUS += "UV, Ozon, "
  if True: AUS = AUS.rsplit(',',1)[0] + " "
  if False: pass

  f = AUS.count(',')
  if   f > 1:
    AUS = ' und'.join(AUS.rsplit(',', 1))
    antwort += AUS + "sind ausgeschaltet. "
  elif f == 1:
    AUS = ' und'.join(AUS.rsplit(',', 1))
    antwort += AUS + "ist ausgeschaltet. "

  if dash_mode == "speak":
    pass
  else:
    antwort = dash_out_xml("aquarium_sensor", "Wassersensor", "OK")
 
  element_alarm('1/2/4', prio, level, reason, action)

  DASH_DATA["t_aqua"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  return level, flag, action, reason, antwort

def dash_aquarium(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm, Blinds

  ATO_level, ATO_flag, ATO_action, ATO_reason, ATO_antwort = dash_dayref(Object)		# Nachfuellanlage
  AQW_level, AQW_flag, AQW_action, AQW_reason, AQW_antwort = dash_wasseraquarium(Object)	# Wassersensor
  TMP_level, TMP_flag, TMP_action, TMP_reason, TMP_antwort = dash_t_aqua(Object)		# H2O Temperatur
  FIL_level, FIL_flag, FIL_action, FIL_reason, FIL_antwort = dash_dayfil(Object)		# Filterpapier

  level = min (ATO_level, AQW_level, TMP_level, FIL_level)

  if   AQW_level < 4:
    antwort = AQW_antwort
    flag    = AQW_flag
  elif TMP_level < 4:
    antwort = TMP_antwort
    flag    = TMP_flag
  elif ATO_level < 4:
    antwort = ATO_antwort
    flag    = ATO_flag
  elif FIL_level < 4:
    antwort = FIL_antwort
    flag    = FIL_flag
  else:
    antwort = "Aquarium alles in Ordnung. "
    flag    = "OK"

  if (Object == "aquarium") or (Object == "details"):
    antwort = AQW_antwort + TMP_antwort + ATO_antwort + FIL_antwort

  if dash_mode == "speak":
    pass
  else:
    antwort = dash_out_xml("aquarium", "Aquarium", flag)
 
  if level < 4: dash_nOKm = dash_nOKm + 1

  DASH_DATA["aquarium"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  return antwort

def dash_centheat(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm, Blinds

  antwort = ""
  level = 4
  if True:
    T1act = ELEM_DATA['1/2/14']["act"]
    T1min = ELEM_DATA['1/2/14']["min"]
    T1max = ELEM_DATA['1/2/14']["max"]
    try:    T1rel = (T1act - T1min) / (T1max - T1min)
    except: T1rel = 0.5

    T2act = ELEM_DATA['1/2/15']["act"]
    T2min = ELEM_DATA['1/2/15']["min"]
    T2max = ELEM_DATA['1/2/15']["max"]
    try:    T2rel = (T2act - T2min) / (T2max - T2min)
    except: T2rel = 0.5

    T3act = ELEM_DATA['1/2/16']["act"]
    T3min = ELEM_DATA['1/2/16']["min"]
    T3max = ELEM_DATA['1/2/16']["max"]
    try:    T3rel = (T3act - T3min) / (T3max - T3min)
    except: T3rel = 0.5

    levelW  = 4
    levelV  = 4
    levelR  = 4
    reasonW = "none"
    reasonV = "none"
    reasonR = "none"
    actionW = "none"
    actionV = "none"
    actionR = "none"

    if (0.0 < T1rel < 1.0) and (0.0 < T2rel < 1.0) and (0.0 < T3rel < 1.0):
      if dash_mode == "speak":
        antwort = antwort + "Die Heizung ist in Ordnung. "
      else:
        antwort = antwort + dash_out_xml("heizung", "Heizung", "OK")

      if ((Object == "heizung") or (Object == "details")) and (dash_mode == "speak"):
        antwort = antwort + "Vorlauf %.0f, Rücklauf %.0f und Wasser %.0f Grad Celsius. " % (T1act, T2act, T3act)
        liste = []
        for R in ROOM_DATA:
          if ROOM_DATA[R]["heat"]["no"] > 0: liste.append(ROOM_DATA[R]["name"])
        if len(liste) == 0:
          antwort = antwort + "Alle Heizkörper in der Wohnung sind aus. "
        else:
          if len(liste) == 1:
            heiz = ', '.join(liste)
            antwort = antwort + "Im Raum {:s} ist die Heizung an. ".format(heiz)
          else:
            heiz = ', '.join(liste)
            heiz = ' und'.join(heiz.rsplit(',', 1))
            antwort = antwort + "Hier ist die Heizung an: " + heiz + ". "

    else:
      dash_nOKm = dash_nOKm + 1
      reason = "open"
      if dash_mode == "speak":
        antwort = antwort + "Heizung ist nicht OK: "
        if not (0.0 < T1rel < 1.0):
          antwort = antwort + "Rücklauf {:.0f}°C. ".format(T1act)
          reasonW = "Rücklauf"
          actionW = "check"
          actionW = "check"
          levelW  = 3 * (1  - (not (-0.1 < T1rel < 1.1)) )
        if not (0.0 < T2rel < 1.0):
          antwort = antwort + "Vorlauf {:.0f}°C. ".format(T2act)
          reasonV = "Vorlauf"
          actionV = "check"
          levelV  = 3 * ( 1 - (not (-0.1 < T2rel < 1.1)) )
        if not (0.0 < T3rel < 1.0):
          antwort = antwort + "Wasser {:.0f}°C. ".format(T3act)
          reasonR = "Wasser"
          actionR = "check"
          levelR  = 3 * ( 1 - (not (-0.1 < T3rel < 1.1)) )
      else:
        heizung = "ALARM: "
        if not (0.0 < T1rel < 1.0): heizung = heizung + "Rücklauf {:.0f}°C".format(T1act)
        if not (0.0 < T2rel < 1.0): heizung = heizung + "Vorlauf {:.0f}°C".format(T2act)
        if not (0.0 < T3rel < 1.0): heizung = heizung + "Wasser {:.0f}°C".format(T3act)
        antwort = antwort + dash_out_xml("heizung", "Heizung", heizung)

    element_alarm('1/2/14', 7, levelW, reasonW, actionW)
    element_alarm('1/2/15', 7, levelV, reasonV, actionV)
    element_alarm('1/2/16', 7, levelR, reasonR, actionR)

  if False: 
    if dash_mode == "speak":
      antwort = antwort + "Fehler bei der Auswertung der Heizung. "
    else:
      antwort = antwort + dash_out_xml("heizung", "Heizung", "Fehler")

  DASH_DATA["centheat"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  return antwort

def dash_fridge(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm

  V = conf_data['Verbosity']['fridge']

  antwort = ""

  notOK = []
  level_min = 4
  for F in conf_data['Type_Lists']['fridge'].split(','):
    flag  = ELEM_DATA[F]['flag']
    prio  = 2 if ELEM_DATA[F]['name'][0] == "G" else 8
    level = 4 if flag == 'green' else 3 if flag == 'yellow' else 0
    level_min = min(level_min, level)
    if level != 4: notOK.append(F)
    element_alarm(F, prio, level, 'hot', 'check')

  if len(notOK) == 0:
    if dash_mode == "speak":
      antwort += "Alle Kühlschränke sind in Ordnung. "
      if Object in ["kühlschrank", "kühlschränke", "kühlschranke", "details"]:
        antwort += f"Oben {ELEM_DATA['1/2/10']['act']:.0f} und {ELEM_DATA['1/2/11']['act']:.0f}, " + \
                   f"unten {ELEM_DATA['1/2/13']['act']:.0f} und {ELEM_DATA['1/2/12']['act']:.0f} Grad Celsius. "
    else:
      antwort += dash_out_xml("fridge", "Kuehlschraenke", "OK")

  else:
    dash_nOKm = dash_nOKm + 1
    Flist = ""
    for F in notOK: Flist += ELEM_DATA[F]['name'] + ", "
    Flist = Flist[:-2]
    if dash_mode == "speak":
      if len(notOK) >  1: Flist = Flist[::-1].replace(',', 'dnu', 1)[::-1] + " sind "
      if len(notOK) == 1: Flist = Flist + " ist "
      if level_min == 3: antwort += "nicht OK. "
      else:              antwort += "kritisch. "

    else:
      if level_min == 3: fridge = "Info: "  + Flist
      else:              fridge = "ALERT: " + Flist
      verbose_print(V,f"Dash text {fridge}")
      antwort = antwort + dash_out_xml("fridge", "Kuehlschraenke", fridge)

  if dash_mode == "xml":
    for F in conf_data['Type_Lists']['fridge'].split(','):
      antwort += dash_out_xml(ELEM_DATA[F]['ID'], ELEM_DATA[F]['name'], f"{ELEM_DATA[F]['act']:.1f}")

  DASH_DATA["fridge"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  return antwort

def dash_inter(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm

  antwort = ""
  alarm = copy.deepcopy(ALARM_OBJ)
  servers = []
  ignore = conf_data["Alarm"]["servers_ignore"].upper()
  for E in ELEM_DATA:
    level = 4
    E_ID = ELEM_DATA[E]["ID"].upper()
    if ELEM_DATA[E]["type"] == "server":
      if (ignore.find(E_ID) == -1) and (ELEM_DATA[E]["act"] == 0):
        servers.append(ELEM_DATA[E]["ID"].title())
        level = 3 if not E in conf_data['alarm2call'] else 0
        reason = "offline"
        action = "check"
      else:
        level = 4
        reason = "none"
        action = "none"
      element_alarm(E, 3, level, reason, action)
    Type  = ELEM_DATA[E]["type"]
    try:    keep  = keep_alive_time[Type]
    except: keep = -1
    try:    alive = time.time() - ELEM_DATA[E]["time"]
    except: alive = 0.0
    if (ignore.find(E_ID) == -1) and (level == 4) and (keep > 0.5) and (alive >= keep * 60.0):
      servers.append(ELEM_DATA[E]["name"].title())

  if True:
    internet = int(FLAT_DATA['inter']['act'])
    if (internet <= 0) and (len(servers) == 0):
      if dash_mode == "speak":
        antwort = antwort + "Internet und Computer sind OK. "
      else:
        antwort = antwort + dash_out_xml("internet", "Internet", "OK")
    else:
      dash_nOKm = dash_nOKm + 1
      info_txt = ""
      if dash_mode == "speak":

        if internet == -1:
          info_txt = "Warnung: Status Internet ist unbekannt. "
        if (internet == 0) and (Object == "internet"):
          info_txt = "Das Internet ist in Ordnung. "
        if internet == 1: info_txt = "Warnung: Internet im Keller nicht in Ordnung. "
        if internet == 2: info_txt = "Warnung: Internet über Stromleitung nicht in Ordnung. "
        if internet == 3: info_txt = "Alarm: Internet im LAN nicht in Ordnung. "
        if internet == 4: info_txt = "Alarm: Internet von Unitymedia nicht in Ordnung. "
        antwort = antwort + info_txt

        if len(servers) > 0:
          if len(servers) == 1:  info_txt = "Der Computer {:s} hat ein Problem. Bitte prüfen. ".format(servers[0])
          else:
            serv_list = ', '.join(servers)
            serv_list = ' und'.join(serv_list.rsplit(',', 1))
            info_txt = "Die Server {:s} haben Probleme. Bitte prüfen. ".format(serv_list)
        else: info_txt = "Alle Server sind OK. "
        antwort = antwort + info_txt
     
      else:
        info = ""
        if   internet == 0: pass
        elif internet == 1: info = "Keller "
        elif internet == 2: info = "Strom "
        elif internet == 3: info = "LAN "
        elif internet == 4: info = "UnityMedia "
        else              : info = f"{internet} undef "

        if   internet == -1: out = "Warn: "  + info_txt + info
        elif internet ==  0: out = "OK "     + info_txt + info
        elif internet ==  1: out = "Info: "  + info_txt + info
        elif internet ==  2: out = "Warn: "  + info_txt + info
        elif internet ==  3: out = "Warn: "  + info_txt + info
        elif internet ==  4: out = "ALARM: " + info_txt + info

        antwort = antwort + dash_out_xml("internet", "Internet", out)

      # antwort = antwort + dash_persons(Object)

  if False:
    if dash_mode == "speak":
      antwort = antwort + "Fehler bei der Auswertung des Internet Status. "
    else:
      antwort = antwort + dash_out_xml("info", "Info System", "Fehler")

  # INTERNET
  level = 4 - max(internet, 0)
  element_alarm('1/2/8', 6, level, 'error', 'check')

  DASH_DATA["inter"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }

  return antwort

def dash_client(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm

  if dash_mode == "speak": return ""

  antwort = ""
  #if knx_group in conf_data['Persons']: antwort = dash_persons(Object)

  clients = []
  for E in ELEM_DATA:
    if (ELEM_DATA[E]['type'] == "client") and (ELEM_DATA[E]['act'] == 1):
      clients.append(ELEM_DATA[E]['ID'])
      
  if len(clients) == 0:
    clients_txt = "none online"
  else:
    clients_txt = '(br)'.join(clients)

  antwort = dash_out_xml("client", "Clients on", clients_txt)
  DASH_DATA["client"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }

  return antwort

def dash_server(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm

  if dash_mode == "speak": return ""

  antwort = ""

  servers = []
  for E in ELEM_DATA:
    if (ELEM_DATA[E]['type'] == "server") and (ELEM_DATA[E]['act'] == 0):
      servers.append(ELEM_DATA[E]['name'])
      
  if len(servers) == 0:
    servers_txt = "all online"
  else:
    servers_txt = '(br)'.join(servers)

  antwort = dash_out_xml("server", "Servers off", servers_txt)
  DASH_DATA["server"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }

  return antwort

def dash_humi(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm

  if dash_mode == "speak": return ""

  antwort = ""

  for E in conf_data['Type_Lists']['humi'].split(','):
    antwort += dash_out_xml("humi_"+E.replace('/','-'), ELEM_DATA[E]['name'], f"{ELEM_DATA[E]['act']/10:.0f}")

  DASH_DATA["humi"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }

  return antwort

def dash_heat(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm

  if dash_mode == "speak": return ""

  antwort = ""

  heats = []
  for E in ELEM_DATA:
    if (ELEM_DATA[E]['type'] == "heat") and (ELEM_DATA[E]['act'] == 1):
      heats.append(ELEM_DATA[E]['name'])
      
  if len(heats) == 0:
    heats_txt = "alle aus"
  else:
    heats_txt = '(br)'.join(heats)

  antwort = dash_out_xml("heat", "radiators off", heats_txt)
  DASH_DATA["heat"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }

  return antwort

def dash_window(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm

  if dash_mode == "speak": return ""

  antwort = ""

  windows = []
  for E in ELEM_DATA:
    if (ELEM_DATA[E]['type'] == "window") and (ELEM_DATA[E]['act'] == 1):
      windows.append(ELEM_DATA[E]['name'])
      
  if len(windows) == 0:
    windows_txt = "alle zu"
  else:
    windows_txt = '(br)'.join(windows)

  antwort = dash_out_xml("window", "radiators off", windows_txt)
  DASH_DATA["window"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }

  return antwort

def dash_person(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm
  global TIMER

  antwort = ""
  home = FLAT_DATA["persons"]['act']
  if True:    num  = 4 - home.count('-')
  if False:
    verbose_print(3,"error in person. setting to ----")
    num = 0
    home = "----"
  alle = []
  if 'D' in home: alle.append("Delia")
  if 'F' in home: alle.append("Fiona")
  if 'V' in home: alle.append("Viviane")
  if 'H' in home: alle.append("Horst")
  if len(alle) != num:
    verbose_print(0, "Error in names")
    verbose_print(0,"ERROR 3 in names " + str(num) + " from persons " + home)
    sys.exit()

  names = ', '.join(alle)
  names = ' und'.join(names.rsplit(',', 1))
  if   num == 0:
    antwort = antwort + "Es ist niemand zu Hause. "
  elif num == 1:
    antwort = antwort + names + " ist zu Hause. "
  else:
    antwort = antwort + names + " sind zu Hause. "

  antwort = antwort + "Im Detail: "
  fiona = duration(time.time() - ELEM_DATA['30/0/52']['time'])
  delia = duration(time.time() - ELEM_DATA['30/0/57']['time'])
  vivia = duration(time.time() - ELEM_DATA['30/0/59']['time'])
  horst = duration(time.time() - ELEM_DATA['30/0/49']['time'])

  if ELEM_DATA['30/0/57']['act'] == 1:
    antwort = antwort + "Delia ist hier seit {:s}. ".format(delia)
  else:
    antwort = antwort + "Delia ist weg seit {:s}. ".format(delia)
  if ELEM_DATA['30/0/52']['act'] == 1:
    antwort = antwort + "Fiona ist hier seit {:s}. ".format(fiona)
  else:
    antwort = antwort + "Fiona ist weg seit {:s}. ".format(fiona)
  if ELEM_DATA['30/0/59']['act'] == 1:
    antwort = antwort + "Viviane ist hier seit {:s}. ".format(vivia)
  else:
    antwort = antwort + "Viviane ist weg seit {:s}. ".format(vivia)
  if ELEM_DATA['30/0/49']['act'] == 1:
    antwort = antwort + "Horst ist hier seit {:s}. ".format(horst)
  else:
    antwort = antwort + "Horst ist weg seit {:s}. ".format(horst)

  # auto lock door if nobody at home or if debug is set and
  # if door is not locked alreay and
  # if door is not yet in TIMER  then
  if ((FLAT_DATA["person"]["act"] == "----") or (conf_data["Debug"]["lock"] == 1))         and \
     (ELEM_DATA['10/2/5']['act'] == 0) and (not '30/7/2' in TIMER):

    TIMER['30/7/2'] = {
      'time': knx_time + conf_data["General"]["auto_lock_wait"] * 60.0,
      'act' : 1,
      'cond_group': '30/7/1',
      'cond_value': 1
    }

#   else:
#     if FLAT_DATA["lock"]["act"] <> 2:		# if Riegel NOT fully closed
#       urllib.urlopen('http://eib.h-wassenberg.de:8065/cgi-bin/eib-home.py?obj=riegel&command=close').read()
#       verbose_print(1,"INFO: Der Türriegel wurde automatisch geschlossen.")

  DASH_DATA["person"]['speak'] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  antwort = dash_out_xml("persons", "Persons", FLAT_DATA["person"]["act"])
  DASH_DATA["person"]['xml']   = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  return antwort

def dash_wetter(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm
  global WEATHER

  antwort = ""
  home = FLAT_DATA["persons"]['act']
  num  = 4 - home.count('-')
  if True:
    w_text = wetter_text[max(wetter_codes[int(WEATHER["w_num"])][2], wetter_codes[int(WEATHER["w_num_0"])][2])]
    temp_outside = round(float(WEATHER["w_T_outside"]))
    temp_text    = "eiskalten "
    if temp_outside >  0.0: temp_text = "kalten "
    if temp_outside > 10.0: temp_text = "kühlen "
    if temp_outside > 10.0: temp_text = "frischen "
    if temp_outside > 15.0: temp_text = "milden "
    if temp_outside > 20.0: temp_text = "angenehmen "
    if temp_outside > 25.0: temp_text = "warmen "
    if temp_outside > 30.0: temp_text = "heißen "
    if temp_outside > 35.0: temp_text = "sehr heißen "
    if dash_mode == "speak":
      if Object == "wetter": antwort = antwort + wetter_codes[int(WEATHER["w_num"])][0] + ". "
      antwort = antwort + w_text + " bei " + temp_text + "{:.0f}".format(temp_outside) + " Grad Celsius. "
    else:
      wetter = ""
      if Object == "wetter": wetter = wetter + wetter_codes[int(WEATHER["w_num"])][0] + ". "
      wetter = wetter + w_text + " bei " + temp_text + "{:.0f}".format(temp_outside) + " °C. "
      antwort = antwort + dash_out_xml("wetter", "Wetter", wetter)
      antwort = antwort + dash_out_xml("brightness", "Brightness", str(FLAT_DATA["bright"]["act"]))

  if False:
    if dash_mode == "speak":
      antwort = antwort + "Fehler bei der Auswertung des Wetters. "
    else:
      verbose_print(2,"ERROR 4 in dash_farewell " + str(num) + " from persons " + home)
      antwort = antwort + dash_out_xml("wetter", "Wetter", "Fehler ")
      antwort = antwort + dash_out_xml("brightness", "Brightness", str(FLAT_DATA["bright"]["act"]))

  DASH_DATA["wetter"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  return antwort

def dash_farewell(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm

  antwort = ""
  hour = datetime.now().hour
  if dash_mode == "speak":
    gruss = "Ich wünsche eine gute Nacht. "
    if hour < 21: gruss = "Ich wünsche einen guten Abend. "
    if hour < 18: gruss = "Ich wünsche einen guten Tag. "
    if hour < 10: gruss = "Ich wünsche einen guten Morgen. "
    if hour <  4: gruss = "Ich wünsche eine gute Nacht. "
    antwort = antwort + gruss
  else:
    gruss = "Ich wuensche eine gute Nacht. "
    if hour < 21: gruss = "Ich wuensche einen guten Abend. "
    if hour < 18: gruss = "Ich wuensche einen guten Tag. "
    if hour < 10: gruss = "Ich wuensche einen guten Morgen. "
    if hour <  4: gruss = "Ich wuensche einen gute Nacht. "
    antwort = antwort + dash_out_xml("fairwell", "Gruss", gruss)

  DASH_DATA["farewell"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  return antwort

def dash_all(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm

  notOKs = ""
  OKlist = ""
  antwort = ""

# if True:    Object = Object.enclode('UTF-8')
# if False: pass
# if True:    Object = str(Object)
# if False: pass

  if Object in [ "kuehlschrank", "kühlschrank", "kühlschränke", "alles", "details"]:
    dash_nOKm = 0
    output = dash_fridge(Object)
    if Object == "alles":
      if dash_nOKm > 0: notOKs = notOKs + output
      else:             OKlist = OKlist + "Kühlschränke, "
    else:
      if (Object == "details"): antwort = antwort + output
      else:                     antwort = output
  
  if Object in [ "heizung", "alles", "details"]:
    dash_nOKm = 0
    output = dash_centheat(Object)
    if Object == "alles":
      if dash_nOKm > 0: notOKs = notOKs + output
      else:             OKlist = OKlist + "Heizung, "
    else:
      if (Object == "details"):
        if True: antwort = antwort + output
        if False:
          print(("decode error:", output))
          sys.exit()
      else:                     antwort = output
  
  if Object in [ "aquarium", "alles", "details"]:
    dash_nOKm = 0
    output = dash_aquarium(Object)
    if Object == "alles":
      if dash_nOKm > 0: notOKs = notOKs + output
      else:             OKlist = OKlist + "Aquarium, "
    else:
      if (Object == "details"):
        if True: antwort = antwort + output
        if False:
          print(("decode error:", output))
          sys.exit()
      else:                     antwort = output
  
  if Object in [ "CO2", "kohlendioxid", "alles", "details"]:
    dash_nOKm = 0
    output = dash_CO2(Object)
    if Object == "alles":
      if dash_nOKm > 0: notOKs = notOKs + output
      else:             OKlist = OKlist + "Kohlendioxid, "
    else:
      if (Object == "details"):
        if True: antwort = antwort + output
        if False:
          print(("decode error:", output))
          sys.exit()
      else:                     antwort = output
  
  if Object in [ "zimmer", "Zimmer", "sender", "zunge", "alles", "details"]:
    if (Object == "sender") or (Object == "zunge"): Object = "zimmer"
    dash_nOKm = 0
    output = dash_zimmer(Object)
    if Object == "alles":
      if dash_nOKm > 0: notOKs = notOKs + output
      else:             OKlist = OKlist + "Zimmer, "
    else:
      if (Object == "details"): antwort = antwort + output
      else:                     antwort = output
  
  if Object in [ "wasser", "alles", "details"]:
    dash_nOKm = 0
    output = dash_water(Object)
    if Object == "alles":
      if dash_nOKm > 0: notOKs = notOKs + output
      else:             OKlist = OKlist + "Wassersensor, "
    else:
      if (Object == "details"): antwort = antwort + output
      else:                     antwort = output
  
  if Object in [ "internet", "netzwerk", "alles", "details"]:
    if (Object == "netzwerk"): Object = "internet"
    dash_nOKm = 0
    output = dash_internet(Object)
    if Object == "alles":
      if dash_nOKm > 0: notOKs = notOKs + output
      else:             OKlist = OKlist + "Internet, "
    else:
      if (Object == "details"): antwort = antwort + output
      else:                     antwort = output
  
  if (Object in [ "personen", "person", "alles", "details"]) and (dash_mode == "speak"):
    dash_nOKm = 0
    output = dash_persons(Object)
    if Object == "alles":
      if dash_nOKm > 0: notOKs = notOKs + output
    else:
      if (Object == "details"): antwort = antwort + output
      else:                     antwort = output
  
  if Object in [ "garage", "garagen", "alles", "details"]:
    dash_nOKm = 0
    output = dash_garage(Object)
    if Object == "alles":
      if dash_nOKm > 0: notOKs = notOKs + output
      else:             OKlist = OKlist + "Garagen, "
    else:
      if (Object == "details"): antwort = antwort + output
      else:                     antwort = output
  
  if Object in [ "wild", "wind", "alles", "details"]:
    if Object == "wild": Object = "wind"

    dash_nOKm = 0
    output = dash_wind(Object)
    if Object == "alles":
      if dash_nOKm > 0: notOKs = notOKs + output
      else:             OKlist = OKlist + "Wind, "
    else:
      if (Object == "details"): antwort = antwort + output
      else:                     antwort = output

  if Object == "alles":
    if OKlist != "":
      if True:
        OKlist = OKlist[:-2] + ". "
        OKlist = ' und'.join(OKlist.rsplit(',', 1))
      if False: pass
      if notOKs == "": antwort = "Alles ist in Ordnung: " + OKlist
      else:            antwort = "Folgendes ist in Ordnung: " + OKlist
    else: antwort = ""
    antwort = antwort + notOKs
  
  if Object in [ "wetter", "alles", "details"]:
    antwort = antwort + dash_wetter(Object)
  
  antwort = antwort + dash_farewell(Object)
  
  return antwort.strip()

def round_it(zahl):
  anz = len("{:.0f}".format(zahl))
  vorn = round(zahl / 10**(anz-2))
  return vorn*10**(anz-2)

def dash_alarm(Object):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, dash_olds, dash_vars, dash_mode, dash_nOKm

  alarm_list = []
  antwort = "Hallo. "

  for R in ROOM_DATA:
    if 0 <= ROOM_DATA[R]["alarm"]["level"] < 4:
      alarm_list.append(R)

  if len(alarm_list) == 0:
    antwort = antwort + "Es gibt keine Alarme. Es ist alles in Ordnung. " + dash_farewell(Object)
  else:
    if len(alarm_list) == 1:
      R            = alarm_list[0]
      room_name    = ROOM_DATA[R]["name"]
      room_trigger = ROOM_DATA[R]["alarm"]["group"]
      room_alarm   = alarm_text(R, room_trigger)
      room_inside  = "im" if room_name[:3] in ["Gan", "Kel", "Ein", "Bad"] else "in"
      antwort = antwort + "Es gibt einen Alarm {:s} {:s}: {:s}".format(room_inside, room_name, room_alarm.replace('Hallo. ', ''))

    else:
      antwort = antwort + "Es gibt {:d} Alarme: ".format(len(alarm_list))
      for R in alarm_list:
        room_name    = ROOM_DATA[R]["name"]
        room_trigger = ROOM_DATA[R]["alarm"]["group"]
        room_alarm   = alarm_text(R, room_trigger)
        room_inside  = "Im " if room_name[:3] in ["Gan", "Kel", "Ein", "Bad"] else "In "
        antwort = antwort + room_inside + room_name + ": " + room_alarm.replace('Hallo. ', '')

    antwort = antwort +  "Danke fürs kümmern. " + dash_farewell(Object)

  verbose_print(1,antwort)

  DASH_DATA["alarm"][dash_mode] = { "speak": antwort, "time": time.time(), "error": dash_nOKm }
  return antwort

#########################
#    WRITE DASH FILE	#
#########################
def write_dash_file():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, DASH_DATA, conf_data
  global dash_olds, dash_mode

  raise Exception("write_dash_file() called but depreciated.")

  dash_mode = "xml"
  dash_new = dash_all("details")
  if dash_new != dash_olds:
    f_dash = open(dash_file + '.tmp', 'w')
    f_dash.write(dash_new + '\n')
    f_dash.close()
    os.system('mv {:s}.tmp {:s}'.format(dash_file, dash_file))
    os.system('wget -q --delete-after http://gate:8061/cgi-bin/updata.py &')
    dash_olds = dash_new
    verbose_print(1,"dash_data updated and triggered on gate")

def dash_out_xml(item, title, value):
  return "<dash_"+item+"_title>"+    title +"</dash_"+item+"_title>\n" + \
         "<dash_"+item+"_value>"+str(value)+"</dash_"+item+"_value>\n"

