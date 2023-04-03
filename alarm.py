# -* coding: utf-8 -*-

def alarm_read(R):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, conf_data

  S_level = ["sehr hoher", "hoher", "mittlerer", "niederiger"]

  try:
    group  = ROOM_DATA[R]["alarm"]["group"]
  except:
    group  = R
    R      = ELEM_DATA[group]['room']

  name   = ELEM_DATA[group]["name"]
  zeit   = ELEM_DATA[group]["alarm"]["time"]
  reason = ELEM_DATA[group]["alarm"]["reason"]
  action = ELEM_DATA[group]["alarm"]["action"]
  level  = ELEM_DATA[group]["alarm"]["level"]
  prio   = ELEM_DATA[group]["alarm"]["prio"]

  if prio == 4:
    speak = "{:s} ist in Ordnung ohne Alarme. ".format(ROOM_DATA[R]['name'])
  else:
    speak  = "In {:s} gibt es einen Alarm mit {:s} Priorität: ".format(ROOM_DATA[R]['name'], S_level[level])
    speak += alarm_text(R, "2/7/3")
    speak = speak.replace("Hallo. ", "")

  return speak

#########################
#     ALARM TEXT        #
#########################
def alarm_text(R, trigger):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, conf_data

  group  = ROOM_DATA[R]["alarm"]["group"]
  name   = ELEM_DATA[group]["name"]
  type   = ELEM_DATA[group]["alarm"]["type"]
  zeit   = ELEM_DATA[group]["alarm"]["time"]
  reason = ELEM_DATA[group]["alarm"]["reason"]
  action = ELEM_DATA[group]["alarm"]["action"]
  level  = ELEM_DATA[group]["alarm"]["level"]
  prio   = ELEM_DATA[group]["alarm"]["prio"]

  if (time.time() - zeit > 1000000.0) and (time.time() - software_start_time > 12.0*60.0):
    print("====================")
    print("1.000 days ", trigger)
    print(time.time() - zeit)
    try:    print(ELEM_DATA[group])
    except: print("trigger =", trigger)
    print("====================")
    ELEM_DATA[group]["alarm"]["time"] = time.time()

  if (ROOM_DATA[R]["alarm"]["level"] < 4) and ((reason == "none") or (action == "none")):
    verbose_print(1,"error in alarm_text for R="+str(R)+" from trigger "+trigger)

  err    = ""
  if type   != ROOM_DATA[R]["alarm"]["type"]:   err = err + "type "
  if zeit   != ROOM_DATA[R]["alarm"]["time"]:   err = err + "time "
  if reason != ROOM_DATA[R]["alarm"]["reason"]: err = err + "reason "
  if action != ROOM_DATA[R]["alarm"]["action"]: err = err + "action "
  if err != "": verbose_print(1,"Error " + err)

  speak  = "Hallo. "

  # --------------------
  #      NOT ALIVE
  # --------------------
  if reason == "not_alive":
    speak = speak + "Das Element {:s}, {:s}, meldet sich seit {:s} nicht mehr. ".format(group.replace('/', ' '), name, duration(time.time()-zeit))
    if action == "check":
      speak = speak + "Bitte prüfen. "
    else:
      speak = speak + "Die Aktion " + action + " ist noch nicht programmiert. "
  # --------------------
  #       WINDOW
  # --------------------
  elif type == "window":
    temp = ROOM_DATA[R]["temp"]["act"]
    humi = ROOM_DATA[R]["humi"]["act"]
    if temp < 0.0: temp = 20.0

    if   reason == "hot":
      speak = speak + "Es ist {:.0f} Grad warm hier. ".format(temp)
    elif reason == "cold":
      speak = speak + "Es ist {:.0f} Grad kalt hier. ".format(temp)
    elif reason == "OK":
      speak = speak + "Die Temperatur ist OK. "
    elif reason == "humid":
      speak = speak + "Die Feuchtigkeit ist mit {:d} % sehr hoch. ".format(int(humi))
    else:
      speak = speak + "Der Grund " + reason + " ist noch nicht programmiert. "
    if   action == "open":
      speak = speak + "Bitte das Fenster öffnen. "
    elif action == "close":
      speak = speak + "Bitte das Fenster schliessen. "
    else:
      speak = speak + "Die Aktion " + action + " ist noch nicht programmiert. "
  # --------------------
  #       GARAGE
  # --------------------
  elif type == "garage":
    if reason == "open":
      speak = speak + "Ein Garagentor ist offen seit "+duration(time.time()-zeit)+". "
    else:
      speak = speak + "Der Grund " + reason + " ist noch nicht programmiert. "
    if action[0:3] == "Tor":
      speak = speak + "Bitte " + action + ". "
    else:
      speak = speak + "Die Aktion " + action + " ist noch nicht programmiert. "
  # --------------------
  #       FRIDGE
  # --------------------
  elif type == "fridge":
    if   trigger == "1/2/10": name = "Kühlschrank oben rechte Seite"
    elif trigger == "1/2/11": name = "Gefrierschrank oben linke Seite"
    elif trigger == "1/2/12": name = "Gefrierschrank unten am Garten"
    elif trigger == "1/2/13": name = "Kühlschrank unten Lorzingseite"
    else:                     name = "Kühlschrank unklar"
    temp = ELEM_DATA[trigger]["act"]
    zeit = ELEM_DATA[trigger]["alarm"]["time"]

    if reason == "hot":
      speak = speak + \
      "Der {:s} ist mit {:.0f} Grad seit {:s} zu warm. ".format(name, temp, duration(time.time()-zeit))
    else:
      speak = speak + "Der Grund " + reason + " ist noch nicht programmiert. "
    if action == "check":
      speak = speak + "Bitte nachsehen. "
    else:
      speak = speak + "Die Aktion " + action + " ist noch nicht programmiert. "
  # --------------------
  #  centrtal HEATING
  # --------------------
  elif type == "centheat":
    if reason in ["Wasser", "Vorlauf", "Rücklauf"]:
      if reason == "Wasser": speak = speak + "Das "
      else                  : speak = speak + "Der "
      speak = speak + reason + " der Heizung ist mit {:.0f} Grad nicht in Ordnung. ".format(ELEM_DATA[trigger]["act"])
    else:
      speak = speak + "Der Grund " + reason + " ist noch nicht programmiert. "
    if action == "check":
      speak = speak + "Bitte die Heizung prüfen. "
    else:
      speak = speak + "Es wurde keine Aktion angegeben. "
  # --------------------
  #       FRIDGE
  # --------------------
  elif type == "fridge":
    if   trigger == "1/2/10": name = "Kühlschrank oben rechte Seite"
    elif trigger == "1/2/11": name = "Gefrierschrank oben linke Seite"
    elif trigger == "1/2/12": name = "Gefrierschrank unten am Garten"
    elif trigger == "1/2/13": name = "Kühlschrank unten Lorzingseite"
    else:                     name = "Kühlschrank unklar"
    temp = ELEM_DATA[trigger]["act"]
    zeit = ELEM_DATA[trigger]["alarm"]["time"]

    if reason == "hot":
      speak = speak + \
      "Der {:s} ist mit {:.0f} Grad seit {:s} zu warm. ".format(name, temp, duration(time.time()-zeit))
    else:
      speak = speak + "Der Grund " + reason + " ist noch nicht programmiert. "
    if action == "check":
      speak = speak + "Bitte nachsehen. "
    else:
      speak = speak + "Die Aktion " + action + " ist noch nicht programmiert. "
  # --------------------
  #        BEAUF
  # --------------------
  elif type == "beauf":
    level = ELEM_DATA[trigger]["alarm"]["level"]
    if reason == "storm":
      if level == 0: speak = speak + "Es gibt Sturm der Stärke {:.0f} mit {:.0f} kmh. ".format( \
                                     FLAT_DATA["beauf"]["beauf_mx"], FLAT_DATA["beauf"]["speed_mx"] )
      else         : speak = speak + "Es gibt Böen der Stärke {:.0f} mit {:.0f} kmh. ".format( \
                                     FLAT_DATA["beauf"]["beauf_mx"], FLAT_DATA["beauf"]["speed_mx"] )
    else:
      speak = speak + "Der Grund " + reason + " ist noch nicht programmiert. "
    if action == "protect":
      speak = speak + "Bitte die Balkone und Jalousien sichern. "
    else:
      speak = speak + "Die Aktion " + action + " ist noch nicht programmiert. "
  # --------------------
  #         DOOR
  # --------------------
  elif type == "door":
    level = ELEM_DATA[trigger]["alarm"]["level"]
    if time.time() - ELEM_DATA[trigger]["time"] > 30.0*24.0*60.0*60:
      verbose_print(1,"ERROR: Die Zeit bei der Wohnungstuer ist nicht konsistent. Bitte pruefen.")
      info_system_mail('ERROR', "Wohnungstuer Zeit {:.0f} falsch".format(time.time()-ELEM_DATA[trigger]["time"]), \
                       '/home/pi/eHome/wohnungstuer_zeit.txt')
      speak = speak + "Die Wohnungstür ist offen. "
    else:
      zeit  = duration(time.time() - ELEM_DATA[trigger]["time"])
      if reason == "open":
        speak = speak + "Die Wohnungstür ist seit {:s} offen. ".format(zeit)
      else:
        speak = speak + "Der Grund " + reason + " ist noch nicht programmiert. "
      if action == "close":
        speak = speak + "Bitte die Tür schließen. "
      else:
        speak = speak + "Die Aktion " + action + " ist noch nicht programmiert. "
  # --------------------
  #        SERVER
  # --------------------
  elif type == "server":
    if reason == "offline":
      dauer = duration(time.time() - ELEM_DATA[group]["alarm"]["time"])
      speak = speak + "Der Computer {:s} ist seit {:s} offline. ".format(ELEM_DATA[group]["ID"], dauer)
    else:
      speak = speak + "Der Grund " + reason + " ist noch nicht programmiert. "
    if action == "check":
      speak = speak + "Bitte prüfen. "
    else:
      speak = speak + "Die Aktion " + action + " ist noch nicht programmiert. "
  # --------------------
  #        WATER
  # --------------------
  elif type == "water":
    if reason == "old":
      dauer = duration(time.time() - ELEM_DATA[trigger]["time"])
      speak = speak + "Letztes Signal vom Wasser Sensor {:s} kam vor {:s}. ".format(ELEM_DATA[group]['name'], dauer)
    elif reason == "water":
      dauer = duration(time.time() - ELEM_DATA[trigger]["alarm"]["time"])
      speak = speak + "Der Wasser Sensor {:s} sieht Wasser seit {:s}. ".format(ELEM_DATA[group]['name'], dauer)
    else:
      speak = speak + "Der Grund " + reason + " ist noch nicht programmiert. "
    if action == "check":
      speak = speak + "Bitte dringend prüfen. "
    else:
      speak = speak + "Die Aktion " + action + " ist noch nicht programmiert. "
  # --------------------
  #       INTERNET
  # --------------------
  elif type == "inter":
    if reason == "error":
      dauer = duration(time.time() - ELEM_DATA[trigger]["time"])
      level = ELEM_DATA['1/2/8']["act"]
      if   level == 4: err = "Unitymedia"
      elif level == 3: err = "LAN intern"
      elif level == 2: err = "LAN Strom"
      elif level == 1: err = "LAN Keller"
      elif level == 0: err = "alles OK"
      else           : err = "unklar"
      speak = speak + "Das Netzwerk {:d} {:s} hat eine Störung seit {:s}. ".format(level, err, dauer)
    else:
      speak = speak + "Der Grund " + reason + " ist noch nicht programmiert. "
    if action == "check":
      speak = speak + "Bitte dringend prüfen. "
    else:
      speak = speak + "Die Aktion " + action + " ist noch nicht programmiert. "
  # --------------------
  #      AQUA TEMP
  # --------------------
  elif (type == "aquarium") or (type == "t_aqua") or (type == "TAQ"):
    TAQ = ELEM_DATA['1/2/4']['act']
    if   reason == "cold":
      speak = speak + "Das Wasser im Aquarium ist {:.1f} Grad Celcius kalt. Bitte Heizung prüfen. ".format(TAQ)
    elif reason == "hot":
      speak = speak + "Das Wasser im Aquarium ist {:.1f} Grad Celcius warm. Bitte Heizung prüfen. ".format(TAQ)
  # --------------------
  #      SERV TEMP
  # --------------------
  elif type == "servt":
    if reason == "hot":
      dauer = duration(time.time() - ELEM_DATA[trigger]["time"])
      tempe = ELEM_DATA[trigger]["act"]
      speak = speak + "Die Temperatur im Serverschrank ist "
      if   level == 2: speak = speak + "mit {:.0f} Grad seit {:s} etwas zu warm. ".format(tempe, dauer)
      elif level == 1: speak = speak + "mit {:.0f} Grad seit {:s} zu warm. ".format(tempe, dauer)
      elif level == 0: speak = speak + "mit {:.0f} Grad seit {:s} viel zu warm. ".format(tempe, dauer)
    else:
      speak = speak + "Der Grund " + reason + " ist noch nicht programmiert. "
    if action == "cool":
      speak = speak + "Bitte dringend die Tür auf machen. "
    else:
      speak = speak + "Die Aktion " + action + " ist noch nicht programmiert. "
  # --------------------
  #        BLINDS
  # --------------------
  elif type == "blinds":
    if (reason == "hot") and (action == "lower"):
      speak = speak + "Es ist warm hier. Die Jalousien könnten vor der Sonne schützen. "
    else:
      speak = speak + "Ursache " + reason + " mit Aktion " + action + " ist noch nicht programmiert. "
  # --------------------
  #    Wasser REFILL
  # --------------------
  elif type == "dayref":
    if action == "refill": speak += "Bitte Nachfüll-Wasser auffüllen. Es ist bald leer. "
    else:                  speak += "Nachfüllanlage Aquarium {:s} unklar. ".format(action)
  # --------------------
  #    Filter erneuern
  # --------------------
  elif type == "dayfil":
    days = (ELEM_DATA['1/2/19']['act'] - time.time()) / 60.0 / 60.0 / 24.0
    if   days <= 0.7: DAYS = "fast leer"
    elif days <= 1.7: DAYS = "in einem Tag leer"
    else:             DAYS = "in {:d} Tagen leer".format(int(days))
    if action == "prepare": speak += "Die Filterrolle Aquarium ist {:s} leer. Bitte Ersatzrolle und Status prüfen. ".format(DAYS)
    else:                   speak += "Alarm Filterrolle Aquarium mit Bitte {:s} unklar. ".format(action)
  # --------------------
  #        LIGHT
  # --------------------
  elif type == "light":
    speak = speak + "Der Typ " + type + " ist noch nicht programmiert. "
    speak = speak + "Die Ursache ist {:s} und die Bitte ist {:s}. Danke. ".format(reason, action)
  # --------------------
  #       INTERNET
  # --------------------
  elif type == "inter":
    speak = speak + "Der Typ " + type + " ist noch nicht programmiert. "
    speak = speak + "Die Ursache ist {:s} und die Bitte ist {:s}. Danke. ".format(reason, action)
  # --------------------
  #      TEMPERATURE
  # --------------------
  elif type == "temp":
    speak = speak + "Der Typ " + type + " ist noch nicht programmiert. "
    speak = speak + "Die Ursache ist {:s} und die Bitte ist {:s}. Danke. ".format(reason, action)
  # --------------------
  #       HUMIDITY
  # --------------------
  elif type == "humi":
    speak = speak + "Der Typ " + type + " ist noch nicht programmiert. "
    speak = speak + "Die Ursache ist {:s} und die Bitte ist {:s}. Danke. ".format(reason, action)
  # --------------------
  #         LOCK
  # --------------------
  elif type == "lock":
    speak = speak + "Der Typ " + type + " ist noch nicht programmiert. "
    speak = speak + "Die Ursache ist {:s} und die Bitte ist {:s}. Danke. ".format(reason, action)
  # --------------------
  #   local  HEATING
  # --------------------
  elif type == "heat":
    speak = speak + "Der Typ " + type + " ist noch nicht programmiert. "
    speak = speak + "Die Ursache ist {:s} und die Bitte ist {:s}. Danke. ".format(reason, action)
  # --------------------
  #   dishwasher
  # --------------------
  elif type == "dish":
    if action == "empty": speak += "Die Spülmaschine ist fertig. Bitte ausräumen. "
    else:                 speak += "Die Aktion " + action + " ist noch nicht programmiert. "
  # --------------------
  #   washing machine
  # --------------------
  elif type == "wash":
    if action == "empty": speak += "Die Waschmaschine ist fertig. Bitte ausräumen. "
    else:                 speak += "Die Aktion " + action + " ist noch nicht programmiert. "
  # --------------------
  #        OTHER
  # --------------------
  else:
    speak = speak + "Der Typ " + type + " ist nicht hinterlegt. Bitte klären. "
    speak = speak + "Die Ursache ist {:s} und die Bitte ist {:s}. Danke. ".format(reason, action)

  return speak

#########################
#     RUN ALARM         #
#########################
def run_alarm(IN_R, IN_trigger):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, conf_data

  V = conf_data["Alarm"]["verbosity"]
  verbose_print(V,"run_alarm IN_R {:d} IN_trigger {:s} {:s}".format(IN_R, IN_trigger, ELEM_DATA[IN_trigger]["name"]))

  R       = IN_R
  trigger = IN_trigger
  verbose_print(5,"run_alarm for room "+str(R)+" with trigger "+trigger)

  try:
    alarm_delay  = conf_data["Room"+str(R)]["alarm_delay"]  * 60
    alarm_repeat = conf_data["Room"+str(R)]["alarm_repeat"] * 60
  except:
    alarm_delay  = conf_data["Alarm"]["alarm_delay"]        * 60
    alarm_repeat = conf_data["Alarm"]["alarm_repeat"]       * 60

  if (R in [1, 2, 5, 6, 8]) and (0 <= FLAT_DATA["alarm"]["level"] < 4):
    verbose_print(5,"from flat")
    level = FLAT_DATA["alarm"]["level"]
    prio  = FLAT_DATA["alarm"]["prio"]
    reason= FLAT_DATA["alarm"]["reason"]
    zeit  = FLAT_DATA["alarm"]["time"]
    alexa = ROOM_DATA[R]["speak"]["time"]
    trigger = FLAT_DATA["alarm"]["group"]
    R       = ELEM_DATA[trigger]["room"]
    verbose_print(5,"from trigger "+trigger)
  else:
    verbose_print(5,"from element")
    level = ROOM_DATA[R]["alarm"]["level"]
    prio  = ROOM_DATA[R]["alarm"]["prio"]
    reason= ROOM_DATA[R]["alarm"]["reason"]
    zeit  = ROOM_DATA[R]["alarm"]["time"]
    alexa = ROOM_DATA[R]["speak"]["time"]
    if 0 <= level < 4: ROOM_DATA[R]["alarm"]["speak"] = time.time()

  # check on valid alarm <> -1 and <> 4
  if 0 <= level < 4:

    dev      = ROOM_DATA[R]["speak"]["dev"]
    desaster = False
    if (level+2*prio <= 5) and (conf_data["Alarm"]["desaster_allow"] == "yes"):
      desaster = True
      dev      = "alle"

    # Waschmaschine und Aquarium
    if trigger in ['4/0/9', '4/0/11']:
      alarm_delay  = 0
      alarm_repeat = 0.5

    # if alarm-status is old enough to be considered and
    # if alarm was not recently announced on Alexa   and
    # if hour is during allowed alarm-time from conf_data
    # or we have a desaster alarm ???
    # alexa =  ROOM_DATA[R]["speak"]["time"] = time.time() # avoid any Alexa Announcement
    # ROOM_DATA[R]["speak"]["time"] = time.time()
    if time.time()-alexa > alarm_repeat:
      verbose_print(V,"Alarm-Data: Level {:d}, Prio {:d}, Text {:s}".format(level, prio, alarm_text(R, trigger)))
      verbose_print(V,"Alarm-Zeit: Zeit {:.1f} min, Alexa {:.1f} min".format((time.time()-zeit)/60.0, (time.time()-alexa)/60.0))

    E = ROOM_DATA[R]["alarm"]["group"]
    if abs(alexa - ELEM_DATA[E]['speak']['time']) > 1.0:
      if not (E in ['1/2/18', '1/2/19', '1/2/4']):
        verbose_print(5,"Error: Dt alexa - ELEM = {:.1f} for {:s} {:s}. Alexa adjusted.".format(alexa - ELEM_DATA[E]['speak']['time'], E, ELEM_DATA[E]['name']))
      alexa = ELEM_DATA[E]['speak']['time']
      ROOM_DATA[R]["speak"]["time"] = alexa
    
    # check time since start of Python code,
    # since last alexa announcement and
    # timing range or desaster alarm
    if (time.time() - software_start_time > 12.0*60.0)                              and \
       (((time.time() - zeit  > alarm_delay ) and (alexa < zeit)) or ((time.time() - alexa > alarm_repeat) and (alexa > zeit))) and \
       (check_time(trigger, "alarm") or (level + 2*prio <= 5)):

      verbose_print(V,"Alarm pre  d1 {:4.1f} d2 {:4.2f} trigger {:s} from {:s}".format(time.time()-zeit, time.time()-alexa, trigger, ROOM_DATA[R]["alarm"]["group"]))
      verbose_print(V,"Alarm_delay {:.1f} Alarm_repeat {:.1f} ELEM Dt {:.1f}".format(alarm_delay, alarm_repeat, time.time()-ELEM_DATA[E]['speak']['time']))

      speak = alarm_text(R, trigger)
      if dev == "alle": speak = speak.replace("Hallo. ", "Durchsage an alle: ")
      verbose_print(1,"Alarm to " + dev + ": " + speak)
      smart_speaker(dev, speak, 0, "cont", R, 2)
      ELEM_DATA[E]["speak"] = { "time": time.time(), "dev": dev }
      room_alarm()
      verbose_print(V,"Alexa of {:s} time updated. Room Alexa now {:4.1f} sec".format(E,time.time()-ROOM_DATA[R]['speak']['time']))

    else:
      reason = "undef"
      if   not (time.time()-zeit  > alarm_delay) : reason = "during delay"
      elif not (time.time()-alexa > alarm_repeat): reason = "wait to repeat"
      elif not check_time(trigger, "alarm")	 : reason = "time not OK"
      elif (time.time() - software_start_time > 60.0) :
        verbose_print(1,"no alarms from {:s} due to fresh start".format(IN_trigger))

      verbose_print(V,"Alarm not announced _delay {:.1f} _repeat {:.1f} dt {:.1f}".format(alarm_delay, alarm_repeat, time.time() - zeit))

#########################
#     ROOM ALARM        #
#########################
def room_alarm():
  global ELEM_DATA, ROOM_DATA, FLAT_DATA

  # clear all existing alarms in the rooms as
  # all will be overwritten by ELEMENT status
  for R in ROOM_DATA: ROOM_DATA[R]["alarm"] = copy.deepcopy(ALARM_OBJ)
  FLAT_DATA["alarm"] = copy.deepcopy(ALARM_OBJ)

  # verbosity level for debugging
  V = conf_data['Alarm']['room_alarm_verbosity']

  # loop through all ELEMENTS
  for E in ELEM_DATA:
    R = ELEM_DATA[E]["room"]
    alarm = copy.deepcopy(ELEM_DATA[E]["alarm"])
   
    if 0 <= alarm["level"] < 4:
      seit = (time.time() - ELEM_DATA[E]['alarm']['time']) / 60.0
      verbose_print(V,"room_alarm: Alarm < 4 found for {:s} in room {:d} since {:.0f} min".format(E, R, seit))
      verbose_print(V,"room_alarm: Alarm < 4 found with level {:d} / prio {:d}".format(alarm["level"], alarm["prio"]))

    if R >= 0:
      totalE = 2*alarm["level"]                 + alarm["prio"]
      totalR = 2*ROOM_DATA[R]["alarm"]["level"] + ROOM_DATA[R]["alarm"]["prio"]
      totalF = 2*FLAT_DATA["alarm"]["level"]    + FLAT_DATA["alarm"]["prio"]

      # if ELEMENT has higher prio than ROOM, then overwrite ROOM with ELEMENT
      if (totalE < totalR) and (0 <= alarm["level"] < 4):
        ROOM_DATA[R]["alarm"] = copy.deepcopy(alarm)
        ROOM_DATA[R]["alarm"]["group"] = E
        try:    ROOM_DATA[R]["speak"]["time"] = ELEM_DATA[E]['speak']['time']
        except:
          ROOM_DATA[R]["speak"]["time"] = -1
          ELEM_DATA[E]['speak'] = { "time": -1, "dev": "nn" }
          verbose_print(1,"ELEM_DATA {:s} Alexa-Record not found and added.".format(E))

      # if ELEMENT has higher prio than FLAT, then overwrite FLAT with ELEMENT
      if ((totalE < totalF) or ((totalE == totalF) and (alarm["prio"] < ROOM_DATA[R]["alarm"]["prio"]))) \
         and (0 <= alarm["level"] < 4) and (totalE < conf_data["Alarm"]["min_total"]):
        FLAT_DATA["alarm"] = copy.deepcopy(alarm)
        FLAT_DATA["alarm"]["group"] = E
        FLAT_DATA["speak"]["time"] = ROOM_DATA[R]['speak']['time']

    else:
      if E != '9/0/99': verbose_print(1,"group " + E + " has invalid room " + str(R))

#########################
#     TOUCH ROOM	#
#########################
def touch_room(R, group):
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, dash_mode

  room = R
  room_alarm()

  found = (0 <= ROOM_DATA[room]["alarm"]["level"] < 4)

  if (room in [1, 2, 5, 6, 8]) and (0 <= FLAT_DATA["alarm"]["level"] < 4):
    found = True
    trigger = FLAT_DATA["alarm"]["group"]
    room = ELEM_DATA[trigger]["room"]

  dT = time.time() - ROOM_DATA[room]["alarm"]["time"]

  if found:
    V = conf_data["Alarm"]["verbosity"]
    verbose_print(V,"Action seen from "+group+" in room "+str(R)+ \
    " alarm on "+ROOM_DATA[room]["alarm"]["type"]+ \
    " group "+ROOM_DATA[room]["alarm"]["group"]+ \
    " reason "+ROOM_DATA[room]["alarm"]["reason"]+ \
    " action " +ROOM_DATA[room]["alarm"]["action"]+ \
    " since " + duration(dT) + ". ")
    run_alarm(R, group)

#########################
#    ELEMENT ALARM      #
#########################
def element_alarm(Group, Prio, Level, reason, action):
  global ELEM_DATA, ROOM_DATA, knx_time

  # check difference existing element versus new alarm
  # exclude time, level, alexa which can change on same alarm
  # include reason and action which form a new alarm
  delta = (ELEM_DATA[Group]["alarm"]["reason"] != reason) or \
          (ELEM_DATA[Group]["alarm"]["action"] != action)

  # reset old alarm if change of relevant alarm occurs
  # and new alarm is more severe (totalE > totalA)
  # and new alarm is not "OK" = level of < 4
  totalE = 2*ELEM_DATA[Group]["alarm"]["level"] + ELEM_DATA[Group]["alarm"]["prio"]
  totalA = 2*Level                              + Prio
  time_E = ELEM_DATA[Group]['alarm']['time']

  if (ELEM_DATA[Group]["alarm"]["level"] < Level) and (Level != 4):
    verbose_print(1,f"error - new alarm level {Level:d} > {ELEM_DATA[Group]['alarm']['level']:d} old but not 4 for "+Group)

  ELEM_DATA[Group]["alarm"] = {
      "time"	: knx_time,
      "group"   : Group,
      "type"    : ELEM_DATA[Group]['type'],
      "prio"	: Prio,
      "level"	: Level,
      "reason"	: reason,
      "action"	: action }

  # keep previous time of alarm if it just became more severe
  if (totalE > totalA) and (not delta):
    ELEM_DATA[Group]["alarm"]["time"] = time_E

  # update alarm in case of change of severness
  if totalE != totalA: touch_room(ELEM_DATA[Group]["room"], Group)

