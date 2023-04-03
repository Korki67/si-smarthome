# handy = German for mobile phone ;-)
# eib_group is a fixed group address and not relevant here
# eib_value is the value provided by the shell script

def update_tri_bt(eib_group, eib_value):
  global HANDY
  Ort = ['location A', 'location B', 'location C', 'location D', 'location E']

  t_act = time.time()
  code = eib_value // 256
  valu = eib_value %  256

  # handy number = line in MAC file
  # see shell script
  handy = code // 10
  if not (handy in [1, 2]):
    verbose_print(1,"Error: only mobile 1+2 are implemented")
  else:
    ort = code %  10
    HANDY[handy][ort] = valu
    TRI_TIME[ort]     = t_act

  # check which location has oldest signal
  # if that is older than threshold in config,
  # then print an information
  t_old = 0
  i_old = -1
  for i in range(5):
    if t_act - TRI_TIME[i] > t_old:
      t_old = t_act - TRI_TIME[i]
      o_old = i
  if t_old > conf_data['General']['tri_max_age'] * 60.0:
    verbose_print(1,"Achtung TRI Daten fehlen von Ort {:d} {:s} seit {:.1f} Minuten.".format(o_old, Ort[o_old], t_old/60.0))

  # compare measured vector of rssi values from all locations
  # to the reference locations and compute error of sum of squares
  # use 24 as max rssi value to avoid n/a value 99 spoils the calculation
  s_min = 100000
  l_min = 'n/a'
  l_old = ELEMENTS_DATA[eib_group]['pos'+str(handy)]
  for loc in HANDY_LOC[handy]:
    s = 0
    for i in range(5): s += (min(24,HANDY[handy][i]) - min(24,HANDY_LOC[handy][loc][i]))**2
    if s < s_min:
      s_min = s
      l_min = loc

  # process and output
  if (ELEMENTS_DATA[eib_group]['pos'+str(handy)] <> l_min) or (conf_data['Handy'+str(handy)]['verbose'] == 1):
    if s_min < conf_data['Handy'+str(handy)]['err_limit']:
      ELEMENTS_DATA[eib_group]['pos'+str(handy)] = l_min
      ELEMENTS_DATA[eib_group]['time'+str(handy)] = time.time()
      if (HANDY[handy] <> [99,99,99,99,99]) and \
        ( (conf_data['Handy'+str(handy)]['verbose'] == 1) or \
          ((conf_data['Handy'+str(handy)]['verbose'] == 2) and (l_min <> l_old)) ):
        verbose_print(1,"Triangulation {:1d} {:16s}: {:2d}, {:2d}, {:2d}, {:2d}, {:2d} OK  {:5d}".format( \
			handy, l_min, HANDY[handy][0], HANDY[handy][1], HANDY[handy][2], HANDY[handy][3], HANDY[handy][4], s_min))
    else:
      if ( (HANDY[handy] <> [99,99,99,99,99]) or (l_old <> "weg")) and \
         ((conf_data['Handy'+str(handy)]['verbose'] == 1) or \
          ((conf_data['Handy'+str(handy)]['verbose'] == 2) and (l_min <> l_old)) ):
        verbose_print(1,"Triangulation {:1d} {:16s}: {:2d}, {:2d}, {:2d}, {:2d}, {:2d} ERR {:5d}".format( \
			handy, l_min, HANDY[handy][0], HANDY[handy][1], HANDY[handy][2], HANDY[handy][3], HANDY[handy][4], s_min))

