#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess, urllib.request, urllib.parse, urllib.error, json, os, math
import time, sys, atexit, pickle, xmltodict, string, copy, datetime as DT
import logging, ssl, calendar, xml.etree.ElementTree as ET
import holidays
from datetime import datetime

os.chdir('/home/pi/si-smarthome')
exec(compile(open('support.py',        "rb").read(), 'support.py',        'exec'))
exec(compile(open('special.py',        "rb").read(), 'special.py',        'exec'))
exec(compile(open('type-update.py',    "rb").read(), 'type-update.py',    'exec'))
exec(compile(open('smart-routines.py', "rb").read(), 'smart-routines.py', 'exec'))
exec(compile(open('room-mode.py',      "rb").read(), 'room-mode.py',      'exec'))
exec(compile(open('write_visu.py',     "rb").read(), 'write_visu.py',     'exec'))
exec(compile(open('dashboard.py',      "rb").read(), 'dashboard.py',      'exec'))
exec(compile(open('alarm.py',          "rb").read(), 'alarm.py',          'exec'))
exec(compile(open('blinds.py',         "rb").read(), 'blinds.py',         'exec'))

###################################################
#            main software parameters		  #
###################################################
software_name           = "eHome-v1.0"
software_version        = 1.0
software_start_time	= time.time()
software_config_time	= -1
conf_file               = "/home/pi/eHome/eHome.conf"
knxt_file               = "/home/pi/siSH/knx_telegram.log"
mess_file               = "/home/pi/siSH/knx_messages.log"
vars_file               = "/home/pi/siSH/siSH-vars.pkl"
JALU_file               = "/home/pi/siSH/jalu.dat"
visu_file               = "/var/www/ehome-html/siSH-data.xml"

###################################################
#           init config + variables		  #
###################################################
conf_data		= {"General": {"verbosity": 1, "verlogity": 1}}
ROOM_DATA		= {}
ELEM_DATA		= {}
DASH_DATA		= {}
LIGHTS			= {}
WEATHER			= {}
TIMER			= {}
dash_mode		= 'speak'
min1_last		= -1
min5_last		= -1
hour_last		= -1
auto_lights_count	= 0
auto_lights_time	= -1

# indoor triangulation
MOBILE			= {
  'TRI': { 1: [99] * 5, 2: [99] * 5, 3: [99] * 5, 4: [99] * 5 },
  'LOC': {1: {}, 2: {}},
  'TIM': [ -1, -1, -1, -1, -1 ]
}
load_vars()
load_conf()
load_weather()

ELEM_DATA['3/0/10']['pos1'] = "weg"
ELEM_DATA['3/0/10']['pos2'] = "weg"

# open pipe to KNX bus and log-file
knx_bus = subprocess.Popen(['knxtool groupsocketlisten', 'ip:192.168.22.65'], \
          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
knx_t = open(knxt_file, 'a')

# initialize variables
act_time  = -1.0
acc_time  =  0.0
off_time  =  0.0
i_loop    =  0
i_hard	  =  0
t_loop    = time.time()
i_real    =  0
i_time    = time.time()

t_visu_xml	= -1
knx_act		= 0
knx_time	= -1
knx_group	= '9/0/99'
knx_change	= False

# infinite main loop
while True:

  # actual 1min / 5min / 1h
  min1_actu = datetime.now().minute
  min5_actu = datetime.now().minute // 5
  hour_actu = datetime.now().hour

  # do 1min items
  if min1_actu != min1_last:
    load_conf()
    save_vars()
    save_JALU()

  # do 5min items
  if min5_actu != min5_last:
    load_weather()			# update weather information
    knx_t.close()			# close & re-open knx telegram logfile
    knx_t = open(knxt_file, 'a')
    check_empty_deebot()		# check to empty deebot with noise
    deebot_sauge_eingang()		# check to hoover entrance in evening

  # calculate & show system load factor
  d_loop = conf_data["General"]["show_loop_time"]
  if (act_time > 0.0) and (d_loop > 0):
    acc_time += time.time() - act_time
    off_time += act_time    - i_time
    i_time    = time.time()

    if i_loop % d_loop == 0:
      average = acc_time / float(d_loop) * 1000.0
      offtime = off_time / float(d_loop) * 1000.0
      tel_min = float(i_loop) / (time.time() - t_loop) * 60.0
      load = average / (average + offtime) * 100.0
      hard = i_hard / d_loop * 100.0
      verbose_print(1, f"loop: {average:8.3f} ms, wait: {offtime:8.3f} ms, telegrams {tel_min:4.1f}/min, hard {hard:4.1f}% load {load:4.1f}%")
      i_loop = 0
      i_hard = 0
      t_loop = time.time()
      acc_time = 0.0
      off_time = 0.0

  # check on bus error and read next line
  if knx_bus.poll() is not None: recover_knx()
  knx_temp = knx_bus.stdout.readline().decode("utf-8")
  act_time = time.time()
  knx_t.write(datetime.now().strftime("%Y.%m.%d; %H:%M:%S; ") + knx_temp)
  knx_read = knx_temp.rstrip().split()
  knx_time = time.time()
  knx_source = "virtual" if (knx_read[2] == '0.0.0') else "hardware"
  i_hard += (knx_source == "hardware")

  # analyse knx group
  knx_group = knx_read[4].rstrip(':')
  if knx_group.count('/') != 2:
    verbose_print(0, "error knx_group: >" + knx_group + "<")
    raise Exception("invalid KNX group without 2 shlashes {:s}".format(knx_group))

  # analyse knx act
  if   len(knx_read) == 6:
    knx_act   = int(knx_read[5], 16)
    knx_alter = 0
  elif len(knx_read) == 7:
    knx_act   = int(knx_read[5], 16) * 256 + int(knx_read[6], 16)
    knx_alter = 0
  elif len(knx_read) == 8:
    knx_act   = int(knx_read[5], 16) * 256 + int(knx_read[6], 16)
    knx_alter = int(knx_read[7], 16)
  elif len(knx_read) == 9:
    knx_act   = int(knx_read[5], 16) * 256 + int(knx_read[6], 16)
    knx_alter = int(knx_read[7], 16) * 256 + int(knx_read[8], 16)
  else:
    raise Exception(f"invalid KNX <{knx_read}> act len {len(knx_read):d}")

  # DEBUG - feed wrong data to check routines
  if (ELEM_DATA[knx_group]['ID'] in conf_data['Debug']) and (knx_alter == 0):
    if conf_data['Debug'][ELEM_DATA[knx_group]['ID']] != "n/a":
      knx_act = conf_data['Debug'][ELEM_DATA[knx_group]['ID']]
      verbose_print(1,f"Debug value {knx_act} sent to {knx_group} {ELEM_DATA[knx_group]['name']}")

  # update ELEMENT in case value (act) changes
  # therefore, last_act always != act
  # and time gives time when current act was set
  knx_change = False
  if ((ELEM_DATA[knx_group]['act'] != knx_act) or (ELEM_DATA[knx_group]['alter'] != knx_alter)) and \
     (knx_group != "9/0/99") and (not ELEM_DATA[knx_group]['type'] in ['fridge', 'centheat']):
    ELEM_DATA[knx_group]['last_time']    = ELEM_DATA[knx_group]['time']
    ELEM_DATA[knx_group]['last_act']     = ELEM_DATA[knx_group]['act']
    ELEM_DATA[knx_group]['last_alter']   = ELEM_DATA[knx_group]['alter']
    ELEM_DATA[knx_group]['last_source']  = ELEM_DATA[knx_group]['source']
    ELEM_DATA[knx_group]['time']	 = knx_time
    ELEM_DATA[knx_group]['act']	         = knx_act
    ELEM_DATA[knx_group]['alter']	 = knx_alter
    ELEM_DATA[knx_group]['source']       = knx_source
    knx_change = True

  # run specials
  special_name = "special_" + knx_group.replace('/', '_')
  special_done = False
  if special_name in globals():
    globals()[special_name]()
    special_done = True

  # run macros
  if knx_group in conf_data['Macros']:
    run_macro(knx_group, knx_act, knx_source)
    knx_group = '9/0/99'
    knx_act   = 0

    # blackout period for auto_lights
    # until macro commands are processed
    # to avoid repeated on-off's
    auto_lights_count = 5

  # update the type with the data
  update_name = "update_" + ELEM_DATA[knx_group]['type']
  update_done = False
  if update_name in globals():
    globals()[update_name]()
    update_done = True

  # run smart routines
  smart_name = "smart_" + ELEM_DATA[knx_group]['type']
  smart_done = False
  if smart_name in globals():
    globals()[smart_name]()
    smart_done = True

  # run dashboard routines to trigger or update alarms
  dash_name = "dash_" + ELEM_DATA[knx_group]['type']
  dash_done = False
  if dash_name in globals():
    dash_mode = "xml"
    globals()[dash_name]("details")
    dash_done = True

  # output command
  if not ELEM_DATA[knx_group]['type'] in ["none", "tri_bt"]:
    if   isinstance(knx_act,   int  ): S_knx_act   = f"{knx_act:5d}"
    elif isinstance(knx_act,   float): S_knx_act   = f"{knx_act:5.1f}"
    elif isinstance(knx_act,   str  ): S_knx_act   = f"{knx_act:<5s}"
    else:raise Exception("type error act   " + str(knx_act))

    if   isinstance(knx_alter, int  ): S_knx_alter = f"{knx_alter:5d}"
    elif isinstance(knx_alter, float): S_knx_alter = f"{knx_alter:5.1f}"
    elif isinstance(knx_alter, str  ): S_knx_alter = f"{knx_alter:<5s}"
    else:raise Exception("type error alter " + str(knx_alter))

    if ((conf_data['Verbosity']['update_done'] == 1) and update_done) or \
       ((conf_data['Verbosity']['smart_done']  == 1) and smart_done ) or \
       ((conf_data['Verbosity']['dash_done']   == 1) and dash_done  ):
      verbose_print(conf_data['General']['knx_verbosity'], \
	f"KNX {knx_source:<8s} {knx_group:8s} {ELEM_DATA[knx_group]['name'][:25]:<25s} " + \
	f"type {ELEM_DATA[knx_group]['type']:<8s} act {S_knx_act:5s} alter {S_knx_alter:5s} " + \
        f"update {update_done:d} smart {smart_done:d} dash {dash_done:d} special {special_done:d}")

  if    auto_lights_count == 0: auto_lights()
  else: auto_lights_count -= 1

  if (knx_time - t_visu_xml > conf_data["General"]["t_eHome_xml"]) and \
     (knx_group != '9/0/99') and (knx_group[0:2] != '30'):
    t_visu_xml = knx_time
    write_visu()

  # run various functions
  run_timer()
  blinds_main_loop()

  # update 1min / 5min / 1h
  min1_last = min1_actu
  min5_last = min5_actu
  hour_last = hour_actu
  i_loop += 1

