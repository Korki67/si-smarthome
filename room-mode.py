# -*- coding: utf-8 -*-

#########################
#     RUN ROOM MODE     #
#########################
def smart_li_mo():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time
  global LIGHTS

  V = conf_data['Verbosity']['room_mode']

  # handle special modes first
  # set group to 9/0/99 to avoid running standard mode process

  # Fernsehen Raum 6 Sued
  if knx_group == '4/3/16':
    if   knx_act == 0:
      knx_group = '4/3/6'
      knx_act = 2
    elif knx_act == 1:
      knx_group = '4/3/6'
      knx_act = 7
    else:
      verbose_print(1,"4/3/16 Wert nicht 0 und nicht 1 = unzulaessig.")

  # Fernsehen Raum 1 Sued
  if (knx_group == '4/3/1') and (knx_act == 7):
    ELEM_DATA['7/2/1']['act']  = 1
    ELEM_DATA['7/2/1']['time'] = knx_time

  if (knx_group == '4/3/1') and (knx_act == 16):
    if ELEM_DATA['4/3/1']['last_act'] == 7:
      os.system('./question "Darf ich das Licht anlassen?" "Licht anlassen?" Sued2 4/3/1 2 > /dev/null &')
      verbose_print(1,"Licht Standard Wohn-Sued nach TV-Ende angefragt.")
      ELEM_DATA['7/2/1']['act'] = 0
      ELEM_DATA['7/2/1']['time'] = knx_time
      TIMER['4/3/1'] = { 'time': knx_time+30, 'value': 0, 'cond_group': "4/3/1", 'cond_value': 2 }
    else:
      verbose_print(1,f"Licht Standard Wohn-Sued nach TV-Ende ignoriert da nicht im TV mode sondern in {ELEM_DATA['4/3/1']['act']:d}.")
      
    knx_group = '9/0/99'
    knx_act   = 0

  if knx_group == '9/0/99': return

  try: speak, radio, loud = LIGHTS[int(knx_act)][knx_group][0].split('*')
  except:
    print(f"knx_act {knx_act:d} knx_group {knx_group:s}")
    print(LIGHTS[int(knx_act)])
    print(LIGHTS[int(knx_act)][knx_group])
    raise Exception("room-mode.py line 11 aborted")

  room = int(knx_group[4:])
  loud = int(loud)
  dev = ROOM_DATA[room]["speak"]["dev"]
  verbose_print(V,"run_room_mode room {:d} knx_act {:d}".format(room, knx_act))
  verbose_print(V,"run_room_mode room {:s} speak {:s}".format(dev, speak))
  if (speak != '-') or (radio != '-'): smart_speaker(dev, speak, loud, radio, room, 6)

  ROOM_DATA[room]['light_mode']['act']  = knx_act
  ROOM_DATA[room]['light_mode']['time'] = knx_time

  # jump into auto_lights to ensure identical knx_time
  auto_lights()

#########################
#	AUTO LIGHT	#
#########################
def auto_lights():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time
  global LIGHTS, WEATHER, BLINDS, auto_lights_time

#  if knx_time - auto_lights_time < conf_data['Lights']['auto_delay']: return
  auto_lights_time = knx_time

  V = conf_data['Verbosity']['auto_lights']

  sun_rise = float(WEATHER['w_sunrise'])
  sun_set  = float(WEATHER['w_sunset'])
  sun_act  = int(0.5 + 100. *(time.time() - sun_rise) / (sun_set - sun_rise))

  for L in ELEM_DATA:
    room = ELEM_DATA[L]["room"]
    if (0 < room < 14) and (L[0:4] != '4/3/'):
      mode = ROOM_DATA[room]["light_mode"]["act"]
      dura = knx_time - ROOM_DATA[room]["light_mode"]["time"]
      try:    unblock_mode = conf_data["Room"+str(room)]["unblock_mode"]
      except: unblock_mode = conf_data["Blinds"]["unblock_mode"]
      if (dura < 0.5) and (unblock_mode == "yes") and (L != '2/4/0'):
        ELEM_DATA[L]["block"] = { "by": '9.0.99', "time": time.time(), "until": -1 }
        if ELEM_DATA[L]['type'] == 'blinds':
          BLINDS[L][1] = -1

      # wenn (Mode 0=<aus>) AND (L in 1=<alles an>) and (Status <> 0):
      if (mode == 0) and (L in LIGHTS[1]) and (dura < 0.001) and (ELEM_DATA[L]["act"] != 0):
        if ELEM_DATA[L]['type'] == 'blinds':
          ELEM_DATA[L]['block']['until'] = -1
          BLINDS[L][1] = -1
        elif ELEM_DATA[L]["ID"][0:3] == 'Dim':
          os.system('groupwrite  ip:192.168.22.65 ' + L + ' 0 > /dev/null')
        else:
          os.system('groupswrite ip:192.168.22.65 ' + L + ' 0 > /dev/null')
        verbose_print(V,"auto-Light {:s} turned off at {:.0f}".format(L, sun_act))
    
      elif (dura < 0.001) or (dura > 10.0) or ((ELEM_DATA[knx_group]['type'] == "mo_li") and knx_change):
        try:
          x = LIGHTS[mode]
          x = ELEM_DATA[L]["block"]["until"]
        except:
          verbose_print(5,"ERROR in {:s} mode {:d}".format(L, mode))
        if (L in LIGHTS[mode]) and (time.time() > ELEM_DATA[L]["block"]["until"]):
          off = LIGHTS[mode][L][1]
          on  = LIGHTS[mode][L][2]
          val = LIGHTS[mode][L][3]
          lux = LIGHTS[mode][L][4]
          if ELEM_DATA[L]['type'] == 'blinds':
            verbose_print(5, "Raff   room {:.0f} mode {:.0f} eib {:s} set {:.0f} lux {:.0f}".format(room, mode, L, val, lux))
            if FLAT_DATA["bright"]["act"] > lux:
              if BLINDS[L][9] > val/100.0:
                BLINDS[L][11] = val/100.0
              BLINDS[L][1] = time.time() + 3.0 * 60.0*60.0

          else:
            # verbose_print(V, "LIGHTS room {:.0f} mode {:.0f} knx {:s} set {:.0f}".format(room, mode, L, val))
            if ((lux == -1) and (off < sun_act < on)) or   \
               ((lux >  -1) and (FLAT_DATA["bright"]["act"] > lux)):
              if ELEM_DATA[L]["act"] != 0:
                if ELEM_DATA[L]["ID"][0:3] == 'Dim':
                  os.system('groupwrite ip:192.168.22.65 ' + L + ' 0 > /dev/null')
                else:
                  os.system('groupswrite  ip:192.168.22.65 ' + L + ' 0 > /dev/null')
                verbose_print(V,"auto-Light {:s} turned off at {:.0f}".format(L, sun_act))
            else:
              if ELEM_DATA[L]["act"] != val:
                if val == 1: os.system('groupswrite ip:192.168.22.65 ' + L + ' 1'               + ' > /dev/null')
                else:        os.system('groupwrite  ip:192.168.22.65 ' + L + ' ' + hex(val)[2:] + ' > /dev/null')
                verbose_print(V,"auto-Light {:s} turned on from {:.0f}".format(L, ELEM_DATA[L]["act"]))

