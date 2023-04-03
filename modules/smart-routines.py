# -*- coding: utf-8 -*-

def smart_window():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  if knx_group == '3/0/6':
    if knx_act == 0:
      os.system('./knx_write 0/0/14 0 &')
    else:
      if ELEM_DATA['1/5/1']['act'] < conf_data['Room1']['balkonlicht_lux']:
        os.system('./knx_write 0/0/14 1 &')

def smart_motion():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['motion']

  # motion Kueche an Kommode TV
  if knx_group == '1/4/19':
    if (check_time(knx_group, 'coffee')) and (ELEM_DATA['4/3/1']['act'] <= 0):
      os.system('./knx_write 4/3/1 2 > /dev/null &')
      smart_speaker("Sued2", "AUTO", 0, "KaffeeAn", 1, 6)
      verbose_print(V,f"Wohn Sued von Mode {ELEM_DATA['4/3/1']['act']:d} auf Auto und Kaffee eingeschaltet.")
    else:
      verbose_print(V,f"Wohn Sued Mode {ELEM_DATA['4/3/1']['act']:d} Auto und Kaffee nicht eingeschaltet.")
      
def door_open(group):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  return

  # open Raffstore at window if in LUT
  # 0       1   2       3           4    5     6    7       8     9    10   11   12   13   14    15   16       17  18
  # Label   Fg  Type    Koordinaten n/a  Speed mode stamp   %stmp %act idx trgt a_v  a_b  x_t   H_t  y_0     reed  %opn

  verbose_print(5, "window open: " + knx_group)
  if knx_group in DOOR_LUT:
    Raff = DOOR_LUT[knx_group]["raff"]
    if BLINDS[Raff][2] == 1:
      Open = float(DOOR_LUT[knx_group]["open"]) / 100.0
      actu = BLINDS[Raff][9]
      verbose_print(2, "1 window {:s} in LUT Raff {:s} open {:.2f} actu {:.2f}".format(knx_group,Raff,Open,actu))
      if (Open > actu + conf_data["BLINDS"]["stop_threshold"]) and (knx_act == 1):
      # if time.time() > BLINDS[Raff][1]:
      # xxxx Horst
        if True:
          BLINDS[Raff][11] = max(Open, actu)
          BLINDS[Raff][1]  = time.time() + 30.0 * 60.0
          #if (BLINDS[Raff][6] != 0) and (knx_act == 1):
          #  ELEM_DATA[knx_group]["act"] = 0
          #  os.system('groupswrite ip:192.168.22.65 ' + knx_group + ' 1 > /dev/null')
          verbose_print(2, "2 window {:s} in LUT Raff {:s} open {:.2f} actu {:.2f}".format(knx_group,Raff,Open,actu))
      if (knx_act < 1) and (time.time() > BLINDS[Raff][1]):
        sun_time = datetime.now() + DT.timedelta(minutes = conf_data["BLINDS"]["anticipate_sun"])  # Vorschau
        sun_raff(Raff, sun_time)
        verbose_print(2, "3 window {:s} in LUT Raff {:s} open {:.2f} actu {:.2f}".format(knx_group,Raff,Open,actu))

def balconies_light(group):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  return

  if ELEM_DATA[knx_group]["act"] == 1:
    SUN_RISE = weather['w_sunrise']
    SUN_SET  = weather['w_sunset']
    if SUN_RISE < time.time() < SUN_SET:
      os.system('./eib ' + knx_group + ' 0 > /dev/null')
      for R in balcony[knx_group]:
        dev = ROOM_DATA[R]["speak"]["dev"]
        dash_mode = "speak"
        speak = "Hallo. Du hast das Licht auf dem Balkon angemacht. Es ist Tag. Daher habe ich es wieder ausgemacht. "
        speak = speak + dash_farewell("detail")
        verbose_print(1,"Info: Licht Balkon aus gemacht. Info an Alexa " + dev)
        loud = 0
        radio = "-"
        alexa_speak(dev, speak, 0, "cont", R, 2)

def blinds_auto_away(group):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  return

  if knx_group in PERSON_DATA:
    txt = ""
    for i_group in PERSON_DATA:
      if ELEM_DATA[i_group]["act"] == 1:
        txt = txt + PERSON_DATA[i_group]["name"][0]
      else:
        txt = txt + '-'
    FLAT_DATA["person"]["act"] = txt
    FLAT_DATA["person"]["time"] = time.time()

  if knx_group == '30/0/52': 			# Fiona
    BLINDS['2/2/0'][2] = 1 - knx_act	# auto if Fiona out
    BLINDS['2/2/0'][2] = 0			# force manual
    define_LUTS()

  if knx_group == '30/0/57': 			# Delia
    BLINDS['2/3/0'][2] = 1 - knx_act	# auto if Delia out
    BLINDS['2/3/0'][2] = 0			# force manual
    define_LUTS()

def smart_t_aqua():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['t_aqua']

  # check water heater on / off
  if ELEM_DATA[knx_group]["act"] > conf_data['Aquarium']['aq_heat_off_at']:
    os.system('./knx_write 7/0/12 0 > /dev/null')
    smart_speaker("Nord1", "AUTO", 0, "AqHeatOff", 1, 6)

    verbose_print(V, f"Water {ELEM_DATA[knx_group]['act']:.1f} above " + \
		     f"threshold {conf_data['Aquarium']['aq_heat_off_at']:.1f}°C. Heater switched off.")

#  if (ELEM_DATA[knx_group]["act"] > conf_data['Aquarium']['aq_heat_off_at'] + 0.1) and \
#     (time.time() - ELEM_DATA['7/0/12']['alarm']['time'] > conf_data['Alarm']['alarm_repeat']*60.0):
#    Dt = (time.time() - ELEM_DATA['7/0/12']['alarm']['time'])/60.0
#    if Dt > conf_data['Aquarium']['warn_freq']:
#      info_system_mail('WARN', "Aquarium zu warm mit {:.1f} Grad C".format(ELEM_DATA[knx_group]["act"]), \
#		       '/home/pi/eHome/aquarium.txt')
#    alarm = copy.deepcopy(ALARM_OBJ)
#    alarm["prio"]   = 4
#    alarm["level"]  = 1
#    alarm["time"]   = time.time()
#    alarm["type"]   = ELEM_DATA['7/0/12']['type']
#    alarm["reason"] = "hot"
#    alarm["action"] = "cool"
#    element_alarm('7/0/12', alarm)
#    ELEM_DATA['7/0/12']['alarm']['time'] = time.time()

  if ELEM_DATA[knx_group]["act"] < conf_data['Aquarium']['aq_heat_on_at']:
    os.system('./knx_write 7/0/12 1 > /dev/null')
    smart_speaker("Nord1", "AUTO", 0, "AqHeatOn", 1, 6)
    verbose_print(V, f"Water {ELEM_DATA[knx_group]['act']:.1f} below " + \
		     f"threshold {conf_data['Aquarium']['aq_heat_on_at']:.1f}°C. Heater switched on.")

#  if (ELEM_DATA[knx_group]["act"] < conf_data['Aquarium']['aq_heat_on_at'] - 0.1) and \
#     (time.time() - ELEM_DATA['7/0/12']['alarm']['time'] > conf_data['Alarm']['alarm_repeat']*60.0):
#    info_system_mail('WARN', "Aquarium zu kalt mit {:.1f} Grad C".format(ELEM_DATA[knx_group]["act"]), '/home/pi/eHome/aquarium.txt')
#    alarm = copy.deepcopy(ALARM_OBJ)
#    alarm["prio"]   = 5
#    alarm["level"]  = 1
#    alarm["time"]   = time.time()
#    alarm["type"]   = ELEM_DATA['7/0/12']['type']
#    alarm["reason"] = "cold"
#    alarm["action"] = "heat"
#    element_alarm('7/0/12', alarm)
#    ELEM_DATA['7/0/12']['alarm']['time'] = time.time()
#
#  if (ELEM_DATA[knx_group]["act"] >= conf_data['Aquarium']['aq_heat_on_at'] - 0.1) and \
#     (ELEM_DATA[knx_group]["act"] <= conf_data['Aquarium']['aq_heat_off_at'] + 0.1):
#    alarm = copy.deepcopy(ALARM_OBJ)
#    alarm["prio"]   = 5
#    alarm["level"]  = 4
#    alarm["time"]   = time.time()
#    alarm["type"]   = ELEM_DATA['7/0/12']['type']
#    alarm["reason"] = "none"
#    alarm["action"] = "none"
#    element_alarm('7/0/12', alarm)
#    ELEM_DATA['7/0/12']['alarm']['time'] = time.time()
#
#  klima(6)

