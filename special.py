# -* coding: utf-8 -*-

def special_0_0_1():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, BLINDS
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  # Licht Eingang kurz bei "fernsehen"
  if (knx_group == '0/0/1') and (knx_act == 1) and (ELEM_DATA['4/3/1']['act'] == 7):
    verbose_print(1,"Licht im Eingang schnell aus im Modus <Fernsehen>")
    os.system('./angle 0/0/1 0 1 2 > /dev/null &')

  # entry same as isle in the night
  special_0_0_17()

def special_7_0_5():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, BLINDS
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  # Licht Esstisch
  if knx_act != 2:
    verbose_print(1,"NFC3 error. Value != 2.")
  else:
    m = ELEM_DATA['0/0/2']['act']
    os.system('./knx_write 0/0/2 ' + str(1-m) + ' > /dev/null')
    ELEM_DATA['0/0/2']["block"]["by"]    = "9.0.99"
    ELEM_DATA['0/0/2']["block"]["time"]  = time.time()
    ELEM_DATA['0/0/2']["block"]["until"] = time.time() + conf_data["General"]["manual_block"] * 60.0*60.0
    verbose_print(1,"NFC3 Licht Esstisch changed from {:d} to {:d}.".format(m, 1-m))

    knx_group = '9/0/99'
    knx_act   = 0

def special_7_0_3():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, BLINDS
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  if knx_act != 2:
    verbose_print(1,"NFC1 error. Value != 2.")
  else:
    v = BLINDS['2/0/0'][9]
    m = BLINDS['2/0/0'][6]
    if m == 0:
      if   v <  0.5:
        os.system('./knx_write 2/0/0 0 > /dev/null')
        BLINDS['2/0/0'][1] = time.time() + 60.0*60.0
        verbose_print(1,"NFC1 Jalu Esstisch moves up.")
      elif v >= 0.5:
        os.system('./knx_write 2/0/0 1 > /dev/null')
        BLINDS['2/0/0'][1] = time.time() + 60.0*60.0
        verbose_print(1,"NFC1 Jalu Esstisch moves down.")
    else:
      verbose_print(1,"NFC1 Jalu Esstisch moving. Not triggered.")

    knx_group = '9/0/99'
    knx_act = 0

def special_4_0_25():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, BLINDS
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  # Home Office Horst mode 3
  # 4/0/25 = power of monitor
  if (knx_act == 1) and (ELEM_DATA['4/3/5']['act'] != 3):
    os.system('./knx_write 4/3/5 3 > /dev/null &')

  if (knx_act == 0) and (ELEM_DATA['4/3/5']['act'] == 3):
    verbose_print(1,"Home Office Horst {:d}, Frage Licht an lassen?".format(knx_act))
    os.system('./question "Darf ich das Licht anlassen?" "Licht anlassen?" Arbeit 4/3/5 2 > /dev/null &')
    TIMER['4/3/5'] = { 'time': knx_time+30, 'value': 0, 'cond_group': "4/3/5", 'cond_value': 2 }

def special_4_0_26():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, BLINDS
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  # Home Office Viviane mode 3
  # 4/0/26 = power of monitor
  if (knx_act == 1) and (ELEM_DATA['4/3/6']['act'] != 3):
    os.system('./knx_write 4/3/6 3 > /dev/null &')

  if (knx_act == 0) and (ELEM_DATA['4/3/6']['act'] == 3):
    verbose_print(1,"Home Office Viviane {:d}, Frage Licht an lassen?".format(knx_act))
    os.system('./question "Darf ich das Licht anlassen?" "Licht anlassen?" Arbeit 4/3/6 2 > /dev/null &')
    TIMER['4/3/6'] = { 'time': knx_time+30, 'value': 0, 'cond_group': "4/3/6", 'cond_value': 2 }

def special_8_0_9():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, BLINDS
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data['Verbosity']['fan']

  # fan Gaeste WC
  humi_all = ROOM_DATA[1]["humi"]["act"]
  humi_bd1 = ROOM_DATA[8]["humi"]["act"]
  humi_bd2 = ROOM_DATA[9]["humi"]["act"]
  humi_bd3 = ROOM_DATA[2]["humi"]["act"]

  fan2         = '0/3/19'
  fan_hyst     = conf_data["Room9"]["fan_hyst"]
  fan_humi     = conf_data["Room9"]["fan_humi"]
  fan_delta    = conf_data["Room9"]["fan_delta"]
  fan_duration = conf_data["Room9"]["fan_duration"]

  if (ELEM_DATA[fan2]["act"] < 1) and \
     (knx_time > ELEM_DATA[fan2]["time"]+fan_duration*60.) and \
     (humi_bd2 > min(fan_humi, humi_all+fan_delta) + fan_hyst):
    os.system('./knx_write '+fan2+' 1 > /dev/null &')
    verbose_print(V,"Info: fan in bad2 switched ON as humidity is high.")

  if (ELEM_DATA[fan2]["act"] == 1) and \
     (knx_time > ELEM_DATA[fan2]["time"]+fan_duration*60.) and \
     (humi_bd2 < min(fan_humi, humi_all+fan_delta) - fan_hyst):
    os.system('./knx_write '+fan2+' 0 > /dev/null &')
    verbose_print(V,"Info: switched fan in bad2 OFF due to timing.")

def special_0_0_17():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, BLINDS
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  # Licht nachts schnell wieder aus
  hour = time.localtime()[3]
  if (knx_act == 1) and (not (6 < hour < 23)):
    delay = conf_data["General"]["quick_off"]
    verbose_print(1,f"Licht {knx_group:s} {ELEM_DATA[knx_group]['name']:s} schnell aus in {delay:.1f}")
    os.system(f"./angle {knx_group:s} 0 1 {delay:.1f} > /dev/null &")

  V = conf_data['Verbosity']['motion']

  # ping in Arbeit wenn Licht Gang nachts an
  MediaOK = check_time('0/0/9', 'bell')
  if (knx_act == 1) and (MediaOK):
    if   (ELEM_DATA['0/0/9']['act'] == 1):
      verbose_print(V,"Bewegung im Gang Info Arbeit")
      os.system('./knx_write 21/0/74 0     &')
      os.system('./knx_write 21/0/74 1 0.6 &')
    elif (ELEM_DATA['4/3/1']['act'] != 0):
      verbose_print(V,"Bewegung im Gang Info Sued")
      os.system('./knx_write 20/0/82 0     &')
      os.system('./knx_write 20/0/82 1 0.6 &')
    else:
      verbose_print(V,"Bewegung im Gang ohne Info da Arbeit und vorne aus.")
  else:
    if knx_act == 1: verbose_print(V,"Bewegung im Gang ohne Info da ausserhalb Zeitfenster.")

