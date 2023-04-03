i_raff = 0

def blinds_main_loop():
  global BLINDS, min1_actu, min1_last, i_raff
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  # handle groups of multiple BLINDS
  if knx_group in BLIND_GROUPS:
    knx_stack = knx_group
    for knx_group in BLIND_GROUPS[knx_stack]:
      ELEM_DATA[knx_group]["source"] = "manual"
      update_blinds()
    knx_group = knx_stack

  # update BLINDS
  blinds_time_sim()
  blinds_statistic()

  if min1_actu != min1_last:
    V = conf_data["Blinds"]["verbosity"]
    mid_day = 0.5 * (int(WEATHER["w_sunset"]) + int(WEATHER["w_sunrise"]))
    hlf_day = 0.5 * (int(WEATHER["w_sunset"]) - int(WEATHER["w_sunrise"]))
    rel_day = 1.0 - max(0, min(1, abs(time.time() - mid_day) / hlf_day))

    sun_time = datetime.now() + DT.timedelta(minutes = int(conf_data["Blinds"]["anticipate_sun"]*rel_day))  # Vorschau
    height, azimuth = sun_position(sun_time)

    FLAT_DATA['sonne'] = "Die Sonne steht bei {:.0f} in einer Höhe von {:.0f} Grad.".format(azimuth, height)
    verbose_print(V,FLAT_DATA['sonne'])

    # find Raffstore with largest delta to target and move this one
    # or process rolling index i_raff % number of blinds
    dp_abs = conf_data["Blinds"]["threshold_move"]
    B_max  = '9/0/99'
    for B in BLIND_KEYS:
      if ELEM_DATA['4/3/'+str(ELEM_DATA[B]['room'])]['act'] != 3:
        case, p = calc_blind_angle(B, sun_time, V)
        if (case == 2) and (p > -0.5) and (abs(BLINDS[B][9] - p) > dp_abs) and (time.time() - BLINDS[B][1] > 0):
          dp_abs = abs(BLINDS[B][9] - p)
          B_max  = B

    Blind = B_max if B_max != '9/0/99' else BLIND_KEYS[i_raff % len(BLIND_KEYS)]
    sun_raff(Blind, sun_time)
    i_raff += 1

# list of groups of blinds
BLIND_GROUPS = {
  "4/1/4": ["2/0/0", "2/0/2", "2/0/4", "2/0/6", "2/1/0", "2/2/0", "2/3/0",  \
            "2/4/0", "2/5/0", "2/5/2", "2/5/4", "2/6/0", "4/1/2"],
  "4/1/5": ["2/0/1", "2/0/3", "2/0/5", "2/0/7", "2/1/1", "2/2/1", "2/3/1",  \
            "2/4/1", "2/5/1", "2/5/3", "2/5/5", "2/6/1", "4/1/3"],
  "4/1/0": ["2/0/0", "2/0/2", "2/0/4", "2/0/6"],
  "4/1/1": ["2/0/1", "2/0/3", "2/0/5", "2/0/7"],
  "4/1/6": ["2/5/0", "2/5/2", "2/5/4"],
  "4/1/7": ["2/5/1", "2/5/3", "2/5/5"],
  "4/4/1": ["2/5/2"]
}

# list of blinds with master data
i0 = -1
BLINDS = {
#            0       1     2     3         4     5   6    7         8    9   10  11    12   13   14    15   16       17  18
# Adresse    Label   ti  auto Koordinaten n/a  Speed mode stamp   %stmp %act idx trgt a_v  a_b  x_t   H_t  y_0     reed  %opn
  "2/0/2" : ["MD4a", i0,   0, "1076,267", 0.0, 70.0, 0, 0000000.0, 1.0, 1.0,  1, -1,  110, 250, 2.0,  0.2, 2.4, '3/0/1', 00],
  "2/0/3" : ["MD4s", i0,   0, "1076,267", 0.0, 70.0, 0, 0000000.0, 1.0, 1.0,  0, -1,  000, 000, 0.0, 00.0, 0.0, '0/0/0', 00],
  "2/0/0" : ["MD3a", i0,   1, "1095,350", 0.0, 40.0, 0, 0000000.0, 1.0, 1.0,  2, -1,  113, 250, 1.4, -0.2, 1.4, '3/0/0', 00],
  "2/0/1" : ["MD3s", i0,   0, "1095,350", 0.0, 40.0, 0, 0000000.0, 1.0, 1.0,  0, -1,  000, 000, 0.0, 00.0, 0.0, '0/0/0', 00],
  "2/0/4" : ["MD1a", i0,   1, "1143,532", 0.0, 60.0, 0, 0000000.0, 1.0, 1.0,  3, -1,  110, 250, 1.4, -0.1, 2.1, '3/0/3', 80],
  "2/0/5" : ["MD1s", i0,   0, "1143,532", 0.0, 60.0, 0, 0000000.0, 1.0, 1.0,  0, -1,  000, 000, 0.0, 00.0, 0.0, '0/0/0', 00],
  "2/0/6" : ["MC4a", i0,   1, "1045,611", 0.0, 60.0, 0, 0000000.0, 1.0, 1.0,  4, -1,  215, 330, 0.7,  0.2, 2.4, '3/0/4', 00],
  "2/0/7" : ["MC4s", i0,   0, "1045,611", 0.0, 60.0, 0, 0000000.0, 1.0, 1.0,  0, -1,  000, 000, 0.0, 00.0, 0.0, '0/0/0', 00],
  "2/1/0" : ["MC1a", i0,   1, "767,480" , 0.0, 40.0, 0, 0000000.0, 1.0, 1.0,  5, -1,  220, 300, 0.3,  0.0, 1.4, '3/1/0', 00],
  "2/1/1" : ["MC1s", i0,   0, "767,480" , 0.0, 40.0, 0, 0000000.0, 1.0, 1.0,  0, -1,  000, 000, 0.0, 00.0, 0.0, '0/0/0', 00],
  "2/2/0" : ["MB4a", i0,   0, "693,480" , 0.0, 60.0, 0, 0000000.0, 1.0, 1.0,  6, -1,  220, 300, 0.3,  0.0, 2.1, '3/2/0', 80],
  "2/2/1" : ["MB4s", i0,   0, "693,480" , 0.0, 60.0, 0, 0000000.0, 1.0, 1.0,  0, -1,  000, 000, 0.0, 00.0, 0.0, '0/0/0', 00],
  "2/3/0" : ["MB3a", i0,   0, "473,480" , 0.0, 60.0, 0, 0000000.0, 1.0, 1.0,  7, -1,  220, 300, 1.0,  0.0, 2.1, '3/3/0', 80],
  "2/3/1" : ["MB3s", i0,   0, "473,480" , 0.0, 60.0, 0, 0000000.0, 1.0, 1.0,  0, -1,  000, 000, 0.0, 00.0, 0.0, '0/0/0', 00],
  "2/4/0" : ["MB2a", i0,   1, "340,480" , 0.0, 40.0, 0, 0000000.0, 1.0, 1.0,  8, -1,  220, 300, 1.0, -0.2, 1.4, '3/4/0', 00],
  "2/4/1" : ["MB2s", i0,   0, "340,480" , 0.0, 40.0, 0, 0000000.0, 1.0, 1.0,  0, -1,  000, 000, 0.0, 00.0, 0.0, '0/0/0', 00],
  "2/5/0" : ["MB1a", i0,   1, "225,480" , 0.0, 60.0, 0, 0000000.0, 1.0, 1.0,  9, -1,  220, 300, 1.0,  0.0, 2.1, '3/5/0', 00],
  "2/5/1" : ["MB1s", i0,   0, "225,480" , 0.0, 60.0, 0, 0000000.0, 1.0, 1.0,  0, -1,  000, 000, 0.0, 00.0, 0.0, '0/0/0', 00],
  "2/5/2" : ["MA3a", i0,   1, "415,140" , 0.0, 60.0, 0, 0000000.0, 1.0, 1.0, 10, -1,   30, 155, 0.2,  0.0, 2.1, '3/5/2', 00],
  "2/5/3" : ["MA3s", i0,   0, "415,140" , 0.0, 60.0, 0, 0000000.0, 1.0, 1.0,  0, -1,  000, 000, 0.0, 00.0, 0.0, '0/0/0', 00],
  "2/5/4" : ["MA4a", i0,   1, "272,192" , 0.0, 60.0, 0, 0000000.0, 1.0, 1.0, 11, -1,   30, 155, 0.2,  0.0, 2.1, '3/5/1', 00],
  "2/5/5" : ["MA4s", i0,   0, "272,192" , 0.0, 60.0, 0, 0000000.0, 1.0, 1.0,  0, -1,  000, 000, 0.0, 00.0, 0.0, '0/0/0', 00],
  "2/6/0" : ["MA2a", i0,   0, "500,140" , 0.0, 60.0, 0, 0000000.0, 1.0, 1.0, 12, -1,   30, 100, 0.2, 00.0, 2.1, '0/0/0', 00],
  "2/6/1" : ["MA2s", i0,   0, "500,140" , 0.0, 60.0, 0, 0000000.0, 1.0, 1.0,  0, -1,  000, 000, 0.0, 00.0, 0.0, '0/0/0', 00],
  "4/1/2" : ["MC2a", i0,   1, "875,480" , 0.0, 60.0, 0, 0000000.0, 1.0, 1.0, 13, -1,  255, 300, 0.5,  0.0, 2.1, '3/0/6', 80],
  "4/1/3" : ["MC2s", i0,   0, "875,480" , 0.0, 60.0, 0, 0000000.0, 1.0, 1.0,  0, -1,  000, 000, 0.0, 00.0, 0.0, '0/0/0', 00]
}

BLIND_OBJ = copy.deepcopy(BLINDS)
BLIND_KEYS = []
DOORS      = {}

def define_LUTS():
  global BLINDS, DOORS
  for R in BLINDS:
    if (BLINDS[R][0][-1] == 'a') and (BLINDS[R][2] == 1):
      BLIND_KEYS.append(R)
    if (BLINDS[R][0][-1] == 'a') and (BLINDS[R][18] > 1):
      DOORS[BLINDS[R][17]] = { "raff": R, "open": BLINDS[R][18] }

define_LUTS()

##########################################################
# receive knx command and update parameters
# to reflect the motion in the real-time simulation
##########################################################
#
def update_blinds():
#            0       1     2     3         4     5   6    7         8    9   10  11    12   13   14    15   16       17  18
# Adresse    Label   ti  auto Koordinaten n/a  Speed mode stamp   %stmp %act idx trgt a_v  a_b  x_t   H_t  y_0     reed  %opn

  global BLINDS
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  # find room of Raffstore
  Room = ELEM_DATA[knx_group]["room"]

  # if EIB command came from a switch and not from the software:
  # lock the raffstore for <manual_break> Minutes
  if ELEM_DATA[knx_group]["source"] == "manual":
    try:    manual_break = conf_data["Room" + str(Room)]["manual_break"]
    except: manual_break = conf_data["Blinds"]["manual_break"]
    BLINDS[knx_group][1] = max(BLINDS[knx_group][1], time.time() + manual_break*60.0)
    BLINDS[knx_group][11] = -1
    verbose_print(1,"raff time lock manually set for {:s} to {:.1f} minutes.".format(knx_group, manual_break))
    touch_room(ELEM_DATA[knx_group]["room"], knx_group)

  R1 = knx_group

  # Start Bewegung 0=hoch oder 1=runter
  if BLINDS[R1][0][-1] == "a":

    # stop previous motion if any
    if BLINDS[R1][6] != 0:
      BLINDS[R1][11] = -1		# target
      verbose_print(3, "Raff case 1 for Raffstore " + R1)

    # start new motion
    BLINDS[R1][6] = knx_act * 2 - 1	# motion
    BLINDS[R1][7] = time.time()		# time
    BLINDS[R1][8] = BLINDS[R1][9]	# stmp? = actual
    verbose_print(3, "Raff case 2 for Raffstore " + R1)

  else: # [0][-1] = "s":
    R2 = R1[:-1] + str(int(R1[-1])-1)		# "a" Raffstore linked to this "s"
    verbose_print(3, "Raff case 0 for Raffstore " + R1 + " => " + R2 + " with " + BLINDS[R2][0][-1])

    # stop previous motion
    if BLINDS[R2][6] != 0:
      BLINDS[R2][6] = 0			# motion
      BLINDS[R2][7] = time.time()	# time
      BLINDS[R2][8] = BLINDS[R2][9]	# stmp? = actual
      BLINDS[R2][11] = -1		# target
      verbose_print(3, "Raff case 5 for Raffstore " + R2)

    # change angle of slats
    else:
      verbose_print(3, "Raff case 6 for Raffstore " + R2)
      pass # to be programmed later

##########################################################
# update real-time simulation of all BLINDS
##########################################################
#
def blinds_time_sim():
#            0       1     2     3         4     5   6    7         8    9   10  11    12   13   14    15   16       17  18
# Adresse    Label   ti  auto Koordinaten n/a  Speed mode stamp   %stmp %act idx trgt a_v  a_b  x_t   H_t  y_0     reed  %opn
  global BLINDS
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  stop_threshold = conf_data["Blinds"]["stop_threshold"]
  for R in BLINDS:

    # if blocked but requested to move then cancel request to move
    if (BLINDS[R][1] > time.time()) and (BLINDS[R][11] > -0.5):
      BLINDS[R][11] = -1

    # if not moving [6] but a target [11] is set different to -1
    if (BLINDS[R][6] == 0) and (BLINDS[R][11] > -0.5):

      # if target requires Raffstore to move up = 0
      if   (time.time()-BLINDS[R][7] > 2.0) and (BLINDS[R][11] > BLINDS[R][9] + stop_threshold*1.5):
        verbose_print(2, "Raff 1 auto {:s} target {:.2f} actual {:.2f}".format(R, BLINDS[R][11], BLINDS[R][9]))
        verbose_print(3, 'x) sending groupswrite ip:192.168.22.65 ' + R + " 0")
        os.system('groupswrite ip:192.168.22.65 ' + R + " 0 > /dev/null &")
        BLINDS[R][7] = time.time()

      # if target requires Raffstore to move down = 1
      elif (time.time()-BLINDS[R][7] > 2.0) and (BLINDS[R][11] < BLINDS[R][9] - stop_threshold*1.5):
        verbose_print(2, "Raff 2 auto {:s} target {:.2f} actual {:.2f}".format(R, BLINDS[R][11], BLINDS[R][9]))
        verbose_print(3, 'y) sending groupswrite ip:192.168.22.65 ' + R + " 1")
        os.system('groupswrite ip:192.168.22.65 ' + R + " 1 > /dev/null &")
        BLINDS[R][7] = time.time()

      # if Raffstore not moving since 2.5 sec then target was too close to actual
      elif (time.time()-BLINDS[R][7] > 2.5):
        verbose_print(4, "z) Raff 2 no auto found {:s} target {:.2f} actual {:.2f}".format(R, BLINDS[R][11], BLINDS[R][9]))
        BLINDS[R][11] = -1		# reset target to "invalid"

    # output status of target only for high verbosity levels
    if BLINDS[R][11] > -0.5:
      verbose_print(4,"Raff 3 auto {:s} target {:.2f} actual {:.2f}".format(R, BLINDS[R][11], BLINDS[R][9]))

    # update real-time simulation data of Raffstore position while moving
    # and stop Raffstore if target position is reached
    if (time.time()-BLINDS[R][7] > 0.0) and (BLINDS[R][6] != 0):
      dt = max(0.0, time.time() - BLINDS[R][7] - conf_data["Blinds"]["offset_time"])
      BLINDS[R][9] = BLINDS[R][8] - BLINDS[R][6] * (dt / BLINDS[R][5])

      # if absolute value of gap < stop_threshold then stop Raffstore by EIB command and in simulation
      if (-0.50 < BLINDS[R][11] < 0.95) and (BLINDS[R][6] * (BLINDS[R][9]-BLINDS[R][11]) < stop_threshold):
        R2 = R[:-1] + str(int(R[-1])+1)				# find "s" linked to this "a" Raffstore
        n_max  = conf_data["Blinds"]["angle_steps"]
        n_wait = conf_data["Blinds"]["angle_wait"]
        a_hori = conf_data["Blinds"]["alpha_hori"]
        a_vert = conf_data["Blinds"]["alpha_vert"]
        room   = ELEM_DATA[R]['room']

        # calculate number of steps to turn slats
        n = int(0.5 + float(n_max)*min(1.0, max(0.0, (WEATHER['sun_height'] - a_vert) / (a_hori - a_vert))))

        # no horizontal angle after down if room > 24 deg
        if ROOM_DATA[1]["temp"]["act"] > 24.0: n = 0

        # afternoon no angle for window facing up to South
        # morning   no angle for window facing up to East
        if (BLINDS[R][12] < 180.0) and (datetime.now().hour > 12): n = n_max
        if (BLINDS[R][12] <  90.0) and (datetime.now().hour < 12): n = 1

        # Arbeit: 0/3/9 depreciated, see home office room 5 below
        if (R == '2/4/0') and (ELEM_DATA['0/3/9']['act'] == 1): n = 1

        # check room mode: Any room mode 7=TV or rooms 5/6 mode 3=home office
        if (ELEM_DATA['4/3/'+str(room)]['act'] == 7) or \
           ((ELEM_DATA['4/3/'+str(room)]['act'] == 3) and (R in [5, 6])):
          n = 0
          BLINDS[R][1] = time.time() + 30.0 * 60.0
          ELEM_DATA[R]['blocked']['until'] = BLINDS[R][1]

        # if Raffstore is moving up/down
        if BLINDS[R][6] == 1:
          if ((BLINDS[R][11] < 0.05) and (abs(BLINDS[R][9] - BLINDS[R][11])) > 0.07) or \
              (BLINDS[R][9] > 0.7):
            n = 0
            n_wait = 0.0
          verbose_print(4, './angle ' + R2 + ' 0 ' + str(1+n) + ' ' + str(n_wait) + ' > /dev/null &')
          os.system('./angle ' + R2 + ' 0 ' + str(1+n) + ' ' + str(n_wait) + ' > /dev/null &')
        else:
          if (abs(BLINDS[R][9] - BLINDS[R][11]) > 0.07) or (BLINDS[R][9] > 0.7):
            n = n_max
            n_wait = 0.0
          verbose_print(4, './angle ' + R2 + ' 1 ' + str(1+n_max-n) + ' ' + str(n_wait) + ' > /dev/null &')
          os.system('./angle ' + R2 + ' 1 ' + str(1+n_max-n) + ' ' + str(n_wait) + ' > /dev/null &')

        # invalidate target [11] if actual position [9] is reasonably close to it
        if abs(BLINDS[R][9] - BLINDS[R][11]) <= 0.07: BLINDS[R][11] = -1
        else:	# gap was below stop_threshold ... so stop should have taken place
          verbose_print(1,"ERROR abs delta 11-9")

      # force simulation into possible boundaries
      if (BLINDS[R][9] > 1.0) or (BLINDS[R][9] < 0.0):
        BLINDS[R][9] = min(max(BLINDS[R][9], 0.0), 1.0)
        BLINDS[R][6] = 0
        BLINDS[R][7] = time.time()
        BLINDS[R][8] = BLINDS[R][9]
        BLINDS[R][11] = -1
        verbose_print(4, "Raff case 0 for Raffstore " + R)

      # transfer simulation from RAFFSTORES to ELEM_DATA and FLAT_DATA
      ELEM_DATA[R]["act"] = int(0.5 + BLINDS[R][9] * 100.)
      ELEM_DATA[R]["time"] = time.time()
      FLAT_DATA["blinds"]["time"] = time.time()

##########################################################
# accumulate BLINDS statistics to ROOM and FLAT
##########################################################
#
def blinds_statistic():
#            0       1     2     3         4     5   6    7         8    9   10  11    12   13   14    15   16       17  18
# Adresse    Label   ti  auto Koordinaten n/a  Speed mode stamp   %stmp %act idx trgt a_v  a_b  x_t   H_t  y_0     reed  %opn
  global ELEM_DATA, ROOM_DATA, FLAT_DATA
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  blinds_all = 0.0
  blinds_tot = 0
  blinds_ave = [0.0] * 20
  blinds_num = [0  ] * 20
  for i_group in BLINDS:
    if ELEM_DATA[i_group]["ID"][-1] == "a":
      if (ELEM_DATA[i_group]["act"] >= -0.5):
        num_room = ELEM_DATA[i_group]["room"]
        blinds_ave[num_room] += ELEM_DATA[i_group]["act"]
        blinds_num[num_room] += 1
        blinds_all = blinds_all + ELEM_DATA[i_group]["act"]
        blinds_tot = blinds_tot + 1

  for i_room in ROOM_DATA:
    if blinds_num[i_room] > 0:
      ROOM_DATA[i_room]["blinds"]["av"] = int( 0.5 + float(blinds_ave[i_room]) / float(blinds_num[i_room]) )
      ROOM_DATA[i_room]["blinds"]["time"] = time.time()
      ROOM_DATA[i_room]["time"] = time.time()
    else:
      ROOM_DATA[i_room]["blinds"]["av"] = -1.0

  if blinds_tot > 0:
    FLAT_DATA["blinds"]["act"] = int( 0.5 + float(blinds_all) / float(blinds_tot) )
    FLAT_DATA["blinds"]["time"] = time.time()
  else:
    FLAT_DATA["blinds"]["act"] = -1.0

##########################################################
# get (case,p) and decide what to do & set target [11]
##########################################################
#
def sun_raff(Raff, sun_time):
#            0       1     2     3         4     5   6    7         8    9   10  11    12   13   14    15   16       17  18
# Adresse    Label   ti  auto Koordinaten n/a  Speed mode stamp   %stmp %act idx trgt a_v  a_b  x_t   H_t  y_0     reed  %opn
  global BLINDS, ELEM_DATA, BLIND_KEYS
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  V = conf_data["Blinds"]["verbosity"]  # local verbosity - level

  a_min = BLINDS[Raff][12]
  a_max = BLINDS[Raff][13]
  x_t   = BLINDS[Raff][14]
  H_t   = BLINDS[Raff][15]
  y_0   = BLINDS[Raff][16]
  Reed  = BLINDS[Raff][17]

  # get position of sun in height + azimuth
  height, azimuth = sun_position(sun_time)

  # if it is an "s" Raffstore than big error and stop to solve
  if BLINDS[Raff][0][-1] == 's':
    verbose_print(0, 'ERROR calling SUN_RAFF ' + Raff)
    sys.exit()

  # get case=scenario and p=percent open
  case, p = calc_blind_angle(Raff, sun_time, V) #1

  # for cases 0 + 1 do nothing
  # if time blocked do nothing
  if (0 <= case < 2) or (BLINDS[Raff][1] > time.time()):
    BLINDS[Raff][11] = -1		# reset the target
    return

  # normal automatic active operation
  elif case == 2:
    BLINDS[Raff][11] = p		# set the target
    BLINDS[Raff][1]  = time.time() + conf_data["Blinds"]["auto_lag_moves"]*60.0

  # move up raffstores and block until 4am if not done yet
  elif (case >= 3) and (BLINDS[Raff][1] < time.time()+5.0*60.0*60.0):
    verbose_print(V, "Raffstore locked until 4am next day for " + Raff)
    now    = datetime.now() + DT.timedelta(days=1)
    future = datetime(now.year, now.month, now.day, 4, 0).timetuple()
    future = time.mktime(future)
    BLINDS[Raff][11] = 1.0			# set to 100% fully open
    BLINDS[Raff][1]  = future		# block until next morning
    BLINDS[Raff][2]  = BLIND_OBJ[Raff][2]	# reset auto-mode on/off
    define_LUTS()
    
  # non-covered case => ERROR
  else:
    verbose_print(1,"ERROR in case calculated" + str(case))

##########################################################
# set sun mode (auto, sun, cloud) for a room manually
# invoced only for 4/0/10 with room x 100 + mode
# mode: 0=auto   1=Sonne   2=Wolken   3=????   4=Nacht
##########################################################
#
def update_sun_auto():
#            0       1     2     3         4     5   6    7         8    9   10  11    12   13   14    15   16       17  18
# Adresse    Label   ti  auto Koordinaten n/a  Speed mode stamp   %stmp %act idx trgt a_v  a_b  x_t   H_t  y_0     reed  %opn
  global ELEM_DATA, ROOM_DATA, FLAT_DATA, WEATHER, Lights
  global knx_group, knx_act, knx_alter, knx_source, knx_time

  room = knx_act // 100
  mode = knx_act %  100
  verbose_print(1,"Sun mode {:d} set for room {:d}".format(mode, room))

  # find all BLINDS in the room and update their parameters
  for R in BLINDS:
    if ELEM_DATA[R]["room"] == room:
      BLINDS[R][1] = -1.0	# reset block time
      BLINDS[R][2] = mode   # set auto
  define_LUTS()

  ROOM_DATA[room]["raff_mode"] = { "no": mode, "time": time.time() }

# HORST

########################################
# calculate blind position and angle
# considering room atmosphere & weather
########################################
# 
def calc_blind_angle(Raff, sun_time, V):
  global BLINDS, ELEM_DATA, ROOM_DATA, FLAT_DATA

  a_min = BLINDS[Raff][12]
  a_max = BLINDS[Raff][13]
  x_t   = BLINDS[Raff][14]
  H_t   = BLINDS[Raff][15]
  y_0   = BLINDS[Raff][16]
  Reed  = BLINDS[Raff][17]
  Ropn  = BLINDS[Raff][18]
  corr  = "none"
  room  = ELEM_DATA[Raff]["room"]

  if Raff in conf_data["Blinds"]["stillgelegt"]:
    ELEM_DATA[Raff]['raff_info'] = "Die Jalousie ist dauerhaft offen. "
    return 2, 1.0

  # get position of sun in height + azimuth
  height, azimuth = sun_position(sun_time)

  # define min-height for morning / afternoon / building
  if sun_time.timetuple().tm_hour < 12:
    h_min = conf_data["Blinds"]["height_morning"]
  else:
    h_min = conf_data["Blinds"]["height_evening"]
  if azimuth > conf_data["Blinds"]["alpha_building"]:
    try:    h_min = conf_data["Room"+str(room)]["height_building"]
    except: h_min = conf_data["Blinds"]["height_building"]

#  hour = time.localtime()[3]
#  if (Raff == '2/4/0') and \
#       ( (ELEM_DATA['4/3/5']['act'] == 3) or \
#         ((ELEM_DATA['4/3/5']['act'] == 2) and not (6 < hour < 20))  \
#       ):
#    ELEM_DATA['2/4/0']['block']['until'] = ELEM_DATA['4/3/5']['block']['until']
#    if time.time() - ELEM_DATA['4/3/5']['time'] < 10.0:
#      BLINDS['2/4/0'][1] = -1.0
#    else:
#      BLINDS['2/4/0'][1] = time.time()+60.0*30.0
#    if BLINDS['2/4/0'][9] < 0.3:
#      p = BLINDS['2/4/0'][9]
#    else:
#      p = 0.0
#
#    return 2, p

  ########################
  # room / blind_mode
  # 0 = auto
  # 1 = Sonne
  # 2 = Wolken
  # 3 = manual
  # 4 = night down
  ########################
  # set room to auto if setting older than 2h
  if (ROOM_DATA[room]["blind_mode"]["time"] + 2.0*60.0*60.0 < time.time()) and (ROOM_DATA[room]["blind_mode"]["act"] < 4):
    ROOM_DATA[room]["blind_mode"]["act"]   = 0		# auto mode
    ROOM_DATA[room]["blind_mode"]["time"] = time.time()	# set time
    verbose_print(1,"Raffstore set to auto mode by time_out: "+Raff)

  # min x_t depending on temperature
  if (ROOM_DATA[room]["temp"]["act"] > 22.0):
    sun_high = conf_data["Blinds"]["sun_high"]
    sun_low  = conf_data["Blinds"]["sun_low"]
    x_t = 0.3 + (x_t - 0.3) * max(0.0, min(1.0, (height - sun_high) / (sun_low - sun_high)))
  # ELEM_DATA[Raff]['raff_info'] = "Ziel ist Schatten {:.1f} Meter Abstand vom Fenster. ".format(x_t)
  ELEM_DATA[Raff]['raff_info'] = ""

  # calculate opening ratio p
  if not (a_min <= azimuth <= a_max):
    p_sun = -1
    corr  = "a_out"
    ELEM_DATA[Raff]['raff_info'] += "Die Sonne scheint nicht auf dieses Fenster. "
  else:
    if abs(y_0) < 0.00001:
      verbose_print(0,"ERROR y_0 = 0 in room " + str(room) + " for " + Raff + " with a_min="+str(a_min))
      p_sun = -1.0
      corr  = "y_0"
    else:
      p_sun = (H_t + math.tan(height*2.*3.1415927 / 360.) * x_t) / y_0
      corr  = "norm"

  # limit p_sun to [0.1 .. 0.9] if valid p_sun
  if p_sun > -0.5: p_sun = max(0.1, min(0.9, p_sun))
  if corr == "norm":
    if abs(p_sun - BLINDS[Raff][9]) > 0.05:
      ELEM_DATA[Raff]['raff_info'] += \
        "Jalousie soll {:.0f} Prozent offen sein, ist aktuell {:.0f} Prozent offen. ".format(p_sun*100, BLINDS[Raff][9]*100)
    else:
      ELEM_DATA[Raff]['raff_info'] += \
        "Jalousie ist gegen die Sonne {:.0f} Prozent offen. ".format(p_sun*100)

  # open in case of door(window) open
  if (ELEM_DATA[Reed]["act"] == 1) and (Ropn > 10):
    if (BLINDS[Raff][18]/100.0 > p_sun):
      p_sun = BLINDS[Raff][18]/100.0
      verbose_print(V+1,"door open, level adjusted for " + Raff)
      corr  = "door"
      ELEM_DATA[Raff]['raff_info'] += "Die Jalousie wurde auf {:.0f} Prozent hochgezogen da die Tür offen ist. ".format(p_sun*100)
    else:
      ELEM_DATA[Raff]['raff_info'] += "Die Jalousie wird nicht wegen des offenen Fensters hochgezogen. "

  # consider room temperature
  T_R = ROOM_DATA[room]["temp"]["act"]
  if T_R < 0.0: T_R = 20.0
  try:    blinds_use_T = conf_data["Room"+str(room)]["blinds_use_T"]
  except: blinds_use_T = conf_data["Blinds"]["blinds_use_T"]
  if T_R < blinds_use_T:
    p_sun = 1.0
    verbose_print(V+1,"room temp {:.1f} below min {:.1f}, raff stay open.".format(T_R,conf_data["Blinds"]["blinds_use_T"]))
    corr  = "r_cold"
    ELEM_DATA[Raff]['raff_info'] += "Die Jalousie wurde hochgezogen, da der Raum unter {:.0f} Grad Celsius kühl ist. ".format(blinds_use_T)

  # consider weather status
  code_descr = { -1: "undefiniert", 0: "keine Sonne", 1: "wenig Sonne", 2: "sonnig", 3: "sehr hell", 4: "super hell"}
  code = WEATHER["w_num"]
  mid_day = 0.5 * (int(WEATHER["w_sunset"]) + int(WEATHER["w_sunrise"]))
  hlf_day = 0.5 * (int(WEATHER["w_sunset"]) - int(WEATHER["w_sunrise"]))
  rel_day = 1.0 - max(0, min(1, abs(time.time() - mid_day) / hlf_day))

  # Korrektur Sun-Level mit Tag (unklar xxx)
  # sun_level = min(wetter_codes[int(code)][3], int(pow(rel_day,0.5)*4.0))
  sun_level = wetter_codes[int(code)][3]

  # read config variables
  try:    blinds_sun_idx  = conf_data["Room"+str(room)]["blinds_sun_idx"]
  except: blinds_sun_idx  = conf_data["Blinds"]["blinds_sun_idx"]
  verbose_print(5,Raff+"sun_idx pos 0 = {:d}".format(blinds_sun_idx))

  try:    blinds_T_red    = conf_data["Room"+str(room)]["blinds_T_red"]
  except: blinds_T_red    = conf_data["Blinds"]["blinds_T_red"]

  try:    blinds_T_inc    = conf_data["Room"+str(room)]["blinds_T_inc"]
  except: blinds_T_inc    = conf_data["Blinds"]["blinds_T_inc"]

  try:    blinds_bright_r = conf_data["Room"+str(room)]["blinds_bright_r"]
  except: blinds_bright_r = conf_data["Blinds"]["blinds_bright_r"]

  try:    blinds_bright_i = conf_data["Room"+str(room)]["blinds_bright_i"]
  except: blinds_bright_i = conf_data["Blinds"]["blinds_bright_i"]

  # KORREKTUR DURCH TEMPERATUR
  idx_T = "sun_idx unchaged by T"
  verbose_print(5,Raff+"sun_idx pos 1 = {:d}".format(blinds_sun_idx))
  ROOM_DATA[room]['raff_idx'] = ""
  if (blinds_T_inc > ROOM_DATA[room]["temp"]["act"]) and (corr != "a_out XXXXX"):
    idx_T = "sun_idx reduced by T"
    blinds_sun_idx += 1
    ROOM_DATA[room]['raff_idx'] += \
      "Der Level wurde wegen niedriger Temperatur von {:.1f} Grad unter Grenze {:.0f} Grad Celsius erhöht. ".format( \
        ROOM_DATA[room]["temp"]["act"], blinds_T_red)

  verbose_print(5,Raff+"sun_idx pos 2 = {:d}".format(blinds_sun_idx))
  if (blinds_T_red < ROOM_DATA[room]["temp"]["act"]) and (corr != "a_out XXXXX"):
    idx_T = "sun_idx increased by T"
    blinds_sun_idx -= 1
    ROOM_DATA[room]['raff_idx'] += \
      "Der Level wurde wegen hoher Temperatur von {:.1f} Grad über Grenze {:.0f} Grad Celsius reduziert. ".format( \
        ROOM_DATA[room]["temp"]["act"], blinds_T_red)
  if (idx_T == "sun_idx unchaged by T"):
    if corr != "a_out XXXXX":
      ROOM_DATA[room]['raff_idx'] += "Die Temperatur liegt mit {:.1f} Grad Celsius im normalen Bereich ".format(ROOM_DATA[room]["temp"]["act"])
      ROOM_DATA[room]['raff_idx'] += "von {:.0f} bis {:.0f} Grad Celsius. ".format(blinds_T_inc, blinds_T_red)
    else:
      ROOM_DATA[room]['raff_idx'] += "Die Sonne strahlt nicht auf dieses Fenster."

  # KORREKTUR DURCH HELLIGKEIT
  verbose_print(5,Raff+"sun_idx pos 3 = {:d}".format(blinds_sun_idx))
  idx_B = "sun_idx unchaged by brightness"
  if (blinds_bright_r < FLAT_DATA["bright"]["act"]) and (corr != "a_out XXX"):
    idx_B = "sun_idx reduced by brightness {:d} to limit {:d}".format(int(FLAT_DATA["bright"]["act"]), int(blinds_bright_r))
    blinds_sun_idx -= 1
    ROOM_DATA[room]['raff_idx'] += \
      "Der Level wurde wegen hoher Helligkeit von {:.0f} über Grenze {:.0f} Lux reduziert. ".format( \
        round_it(FLAT_DATA["bright"]["act"]), round_it(blinds_bright_r))

  verbose_print(5,Raff+"sun_idx pos 4 = {:d}".format(blinds_sun_idx))
  if (blinds_bright_i > FLAT_DATA["bright"]["act"]) and (corr != "a_out XXX"):
    idx_B = "sun_idx increased by brightness {:d} to limit {:d}".format(int(FLAT_DATA["bright"]["act"]), int(blinds_bright_i))
    blinds_sun_idx += 1
    ROOM_DATA[room]['raff_idx'] += \
      "Der Level wurde wegen niedriger Helligkeit von {:.0f} unter Grenze {:.0f} Lux erhöht. ".format( \
        round_it(FLAT_DATA["bright"]["act"]), round_it(blinds_bright_i))
  if (idx_B == "sun_idx unchaged by brightness"):
    ROOM_DATA[room]['raff_idx'] += "Die Helligkeit liegt mit {:.0f} Lux im normalen Bereich von {:.0f} bis {:.0f} Lux. ".format( \
        FLAT_DATA["bright"]["act"], blinds_bright_i, blinds_bright_r)

  if (idx_T == "sun_idx unchaged by T") and (idx_B == "sun_idx unchaged by brightness"):
    pass

  verbose_print(5,Raff+"sun_idx pos 5 = {:d}".format(blinds_sun_idx))

  # delay change of blinds_sun_idx 30min xxxx new feature!
  #try:
  #  if ELEM_DATA[Raff]['blinds_sun_idx']['time'] < time.time():
  #    ELEM_DATA[Raff]['blinds_sun_idx']['time']  = time.time() + 30.0*60.0
  #    ELEM_DATA[Raff]['blinds_sun_idx']['value'] = blinds_sun_idx
  #    verbose_print(5,"blinds_sun_idx stored for {:s}".format(Raff))
  #  else:
  #    blinds_sun_idx = ELEM_DATA[Raff]['blinds_sun_idx']['value']
  #    verbose_print(5,"blinds_sun_idx recovered for {:s}".format(Raff))
  #except:
  #   ELEM_DATA[Raff]['blinds_sun_idx'] = {'time': -1, 'value': blinds_sun_idx}

  # ???????????????? keine Ahnung wo das genutzt wird ???????????????????????
  ELEM_DATA[Raff]['blinds_sun_idx'] = {'time': -1, 'value': blinds_sun_idx}

  verbose_print(conf_data["Blinds"]["verbosity"],"Room "+str(room) + ": " + idx_T + " // " + idx_B)

  ROOM_DATA[room]['raff_room'] = "Der Tag ist bei {:.0f} Prozent. ".format(rel_day*100)
  if not (-1 <= sun_level <= 3) and (corr != "a_out"):
    ELEM_DATA[Raff]['raff_info'] += "Fehler: Sonnenstärke ist mit Wert {:d} unklar. ".format(sun_level)

  verbose_print(V,"code: {:s} sun_level: {:d}, sun_idx: {:d}, sun_mode_act: {:d}, D_t: {:.2f}".format( \
                   code, sun_level, blinds_sun_idx,           \
                   ROOM_DATA[room]['blind_mode']['act'],                                 \
                   (time.time()-ROOM_DATA[room]['blind_mode']['time'])/60.0/60.0))

  # if ((sun_act < sun_conf) and not (command "Sonne" within last 2h)) OR
  # if (command "Wolken" within last 2h) then blinds up = 1.0
  ROOM_DATA[room]['sonne_info'] = ""
  if ((sun_level < blinds_sun_idx) and \
      not ((ROOM_DATA[room]['blind_mode']['act'] == 1) and (time.time()-ROOM_DATA[room]['blind_mode']['time'] < 2.0*60.0*60.0))) or \
     ((ROOM_DATA[room]['blind_mode']['act'] == 2) and (time.time()-ROOM_DATA[room]['blind_mode']['time'] < 2.0*60.0*60.0)):
    p_sun = 1.0
    if (-1 <= sun_level <= 3) and (-1 <= blinds_sun_idx <= 4):
      if ROOM_DATA[room]['blind_mode']['act'] != 2:
        ROOM_DATA[room]['sonne_info'] = "Die Sonnenstärke ist mit {:d} {:s} unter Vorgabe {:d} {:s}. Daher bleiben die Jalousien auf. ".format( \
        sun_level, code_descr[sun_level], blinds_sun_idx, code_descr[blinds_sun_idx])
    else:
      ROOM_DATA[room]['sonne_info'] = "Fehler: Index 1 ist {:d} und Index 2 ist {:d} . ".format(sun_level, blinds_sun_idx)
    corr  = "clouds"
    verbose_print(V+1,"sun level too low: "+str(sun_level)+" conf: "+str(conf_data["Blinds"]["blinds_sun_idx"]))
  else:
    ROOM_DATA[room]['sonne_info'] = "Die Sonnenstärke ist auf Vorgabe {:d} {:s}. Daher passen sich die Jalousien an. ".format( \
        blinds_sun_idx, code_descr[blinds_sun_idx])
    verbose_print(V+1, Raff+" clouds: "+str(sun_level)+" p_sun:" + str(p_sun) + " corr: " + corr + " mode: "+ \
        str(ROOM_DATA[room]['blind_mode']['act'])+" time: "+str(time.time()-ROOM_DATA[room]['blind_mode']['time']))
    
  # ---------------------------------------
  # analyse different cases of sun position
  # ---------------------------------------
  # pre-set error values
  raff_case = -1
  p = -2.0

  # case 0 = before a_min
  if azimuth < a_min:
    raff_case = 0
    p = -1.0

  # case 1 = before a_max with height too low but rising
  elif (azimuth < a_max) and (height < h_min) and (time.time() < mid_day):
    raff_case = 1
    p = -1.0

  # case 2 = before a_max with height OK with sun rising or falling
  elif (azimuth < a_max) and (h_min <= height):
    raff_case = 2
    p = p_sun

  # case 3 = before a_max with height too low and falling
  elif (azimuth < a_max) and (height < h_min) and (mid_day <= time.time()):
    raff_case = 3
    p = -1.0

  # case 4 = after a_max
  elif a_max <= azimuth:
    raff_case = 4
    p = -1.0

  else:
    raff_case = -1
    p         = -1.0
    verbose_print(1,"ERROR in calc_blind_angle case conditions")

  # if mode == 3 manual then set target to invalid
  if ROOM_DATA[room]['blind_mode']['act'] == 3:
    p     = -1.0
    corr  = "manual"
    ELEM_DATA[Raff]['raff_info'] += "Die Automatik ist hier aus. Die Jalousie wird nicht automatisch bewegt. "

  if BLINDS[Raff][1] < time.time():
    verbose_print(V,"raffstore calc {:d}: {:.5s} a_min {:5.1f} a_max "              \
                    "{:5.1f} x_t {:4.1f} H_t {:4.1f} y_0 {:4.1f} Reed "             \
                    "{:.5s} hi {:6.2f} az {:5.1f} p {:5.2f} {:s}".format(raff_case, \
                    Raff,a_min, a_max, x_t, H_t, y_0, Reed, height, azimuth, p, corr))
  else:
    p = -1.0
    zeit = BLINDS[Raff][1] - time.time()
    if (zeit < 3600.0):
      zeit = "{:.0f} Minuten ".format(zeit/60.0)
    else:
      zeit = "{:.1f} Stunden ".format(zeit/3600.0)
    ELEM_DATA[Raff]['raff_info'] += "Sie ist noch {:s} blockiert. ".format(zeit)

  # Unklar - add Text later ... xxxxxx
  if (FLAT_DATA["lock"]["act"] == 2) and (float(WEATHER['w_T_outside']) > conf_data["Blinds"]["outer_temp_close_raff_door_locked"]):
    if p < 0.9: p = 0.0

  return raff_case, p

######################################
#           SAVE JALU                #
######################################
def sort_KEY(E):
  p1 = E.find('/')
  p2 = E.find('/', p1+1)
  i1 = int(E[:p1])
  i2 = int(E[p1+1:p2])
  i3 = int(E[p2+1:])
  return i1*100**2 + i2*100**1 + i3*100**0

def save_JALU():
  global ROOM_DATA, MTBM_file_a, MTBM_file_r, ELEM_DATA
  global JALU_file

  E_sort = sorted(ELEM_DATA.keys(),key=sort_KEY)
  JALU_dat = datetime.now().strftime("%Y.%m.%d; %H:%M:%S; ")

  for E in E_sort:
    R = ELEM_DATA[E]['room']
    try:
      if (ELEM_DATA[E]['ID'][0] == "M") and (ELEM_DATA[E]['ID'][3] == "a") and (len(ELEM_DATA[E]['ID']) == 4):
        JALU_dat += "{:3d}; ".format(ELEM_DATA[E]['act'])
    except: pass

  # kontinuierle Aufschreibung Jalu pro Raum eine Zeile
  file = open (JALU_file, 'a')
  file.write(JALU_dat + "\n")
  file.close()

