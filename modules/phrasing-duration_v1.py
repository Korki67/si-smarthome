import datetime as DT
import calendar
 
def duration(input_T, accu="normal"):
 
  delta_T = input_T
 
  # ------------------------------------
  # break down into days, hors, min, sec
  # ------------------------------------
  t_o = DT.datetime.fromtimestamp(time.time() - input_T)
  t_n = DT.datetime.fromtimestamp(time.time())
 
  seconds = t_n.second  - t_o.second
  minutes = t_n.minute  - t_o.minute
  hours   = t_n.hour    - t_o.hour
  days    = t_n.day     - t_o.day
  month   = t_n.month   - t_o.month
  years   = t_n.year    - t_o.year
 
  if seconds < 0:
    seconds += 60
    minutes -=  1
  if minutes < 0:
    minutes += 60
    hours   -=  1
  if hours < 0:
    hours  += 24
    days   -= 1
  if days < 0:
    prev_month = t_n.replace(day=1) - DT.timedelta(days=1)
    days   += calendar.monthrange(prev_month.year, prev_month.month)[1]
    month  -= 1
  if month < 0:
    month  += 12
    years  -= 1
    
  seconds0 = seconds
  minutes0 = minutes
  hours0   = hours
  days0    = days
  month0   = month
  years0   = years
 
  # ------------------------------------
  # roand small / high numbers
  # ------------------------------------
  if (minutes > 0) and (seconds < 10): seconds = 0
 
  if seconds > 50:
    seconds = 0
    minutes += 1
 
  if ((hours  >  0) and (minutes <  5)) or \
     ((hours  >  3) and (minutes < 10)) or \
     ((hours  >  7) and (minutes < 15)):
    minutes = 0
    seconds = 0
 
  if ((hours  >  0) and (minutes > 55)) or \
     ((hours  >  2) and (minutes > 50)) or \
     ((hours  >  7) and (minutes > 45)):
    minutes = 0
    seconds = 0
    hours   += 1
 
  if (days   > 0) and (hours   <  3): hours   = 0
 
  if (days   > 0) and (hours   > 21):
    hours   = 0
    days    += 1
 
  if   years > 0:
    if days > 15:
      month += 1
      days   = 0
    else:
      days   = 0
 
  elif month > 0:
    if hours > 12:
      days += 1
      hours = 0
    else:
      hours = 0
 
  elif days  > 0:
    if minutes >= 30:
      hours += 1
      minutes= 0
    else:
      minutes= 0
 
  elif hours > 0:
    if seconds >= 30:
      minutes += 1
      seconds  = 0
    else:
      seconds  = 0
 
  elif minutes > 0:
    if seconds >= 40:
      minutes += 1
      seconds  = 0
 
  if (hours  > 1):
    min10 = int((minutes+5.0)/10.)*10
    min15 = int((minutes+7.5)/15.)*15
    if abs(min15 - minutes) < abs(min10 - minutes):
      minutes = min15
    else:
      minutes = min10
    seconds = 0
 
  # corrections
  if minutes >= 60:
    minutes -= 60
    hours   += 1
  if hours >= 24:
    hours   -= 24
    days    += 1
  prev_month = t_n.replace(day=1) - DT.timedelta(days=1)
  prev_days  = calendar.monthrange(prev_month.year, prev_month.month)[1]
  if days  > prev_days:
    days    -= prev_days
    month   += 1
  if month >= 12:
    month   -= 12
    years   += 1
 
  # adjust accuracy
  if accu == "low":
    
    if minutes > 0:
      seconds = ((seconds+15) // 30) * 30
      if (seconds == 60) or ((minutes > 3) and (seconds == 30)):
        if seconds0 >= 30: minutes  += 1
        seconds   = 0
 
    if hours > 0:
      minutes = ((minutes+15) // 30) * 30
      if (minutes == 60) or ((hours > 3) and (minutes == 30)):
        if minutes0 >= 30: hours   += 1
        minutes  = 0
 
    if days > 0:
      hours = ((hours+6) // 12) * 12
      if (hours == 24) or ((days > 3) and (hours == 12)):
        if hours0 >= 12: days  += 1
        hours  = 0
    
    if month > 0:
      days = ((days+7) // 15) * 15
      if (days == 30) or ((month > 4) and (days == 15)):
        if days0 >= 15: month += 1
        days   = 0
    
    if years > 0:
      month = ((month+3) // 6) * 6
      if (month == 12) or ((years > 3) and (month == 6)):
        if month0 >= 6: years += 1
        month  = 0
    
    if (years == 0) and (month > 9) and (days == 0):
      years += 1
      month  = 0
  
    if (month == 0) and (days > 20) and (hours == 0):
      month += 1
      days   = 0
 
    if (days == 0) and (hours > 18) and (minutes == 0):
      days  += 1
      hours  = 0
 
    if (days == 0) and (9 < hours <= 18) and (minutes == 0):
      hours  = 12
 
    if (hours == 0) and (minutes > 44) and (seconds == 0):
      hours   += 1
      minutes  = 0
 
    if (hours == 0) and (20 < minutes <= 44) and (seconds == 0):
      minutes  = 30
 
  # ------------------------------------
  # convert to text
  # ------------------------------------
  if   years > 0:
    if   years == 1: output = "1 year and "
    else:            output = "{:d} years and ".format(years)
    if   month == 0: output = output.replace(' and ', '')
    elif month == 1: output = output + "1 month".format(month)
    elif 4 < month < 8:
      output = output.replace('1 year and ', '1 and a half years')
      output = output.replace(' years and ', ' and a half years')
    else:            output = output + "{:d} months".format(month)
 
  elif month > 0:
    if   month == 1: output = "1 month and "
    else:            output = "{:d} months and ".format(month)
    if   days  == 0: output = output.replace(' and ', '')
    elif days  == 1: output = output + "1 day".format(days)
    elif 12 < days < 18:
      output = output.replace('1 month and ', '1 and a half months')
      output = output.replace(' month and ', ' and a half months')
    else:            output = output + "{:d} days".format(days)
 
  elif days > 0:
    if   days == 1:  output = "1 day and "
    else:            output = "{:.0f} days and ".format(days)
    if   hours == 0: output = output.replace(' and ', '')
    elif hours == 1: output = output + "1 hour".format(hours)
    elif 9 < hours < 15:
      output = output.replace('1 day and ', '1 and a half days')
      output = output.replace(' days and ', ' and a half days')
    else:            output = output + "{:.0f} hours".format(hours)
 
  elif hours > 0:
    if hours     == 1: output = "1 hour and "
    else:              output = "{:.0f} hours and ".format(hours)
    if   minutes == 0: output = output.replace(' and ', '')
    elif minutes == 1: output = output + "1 minute"
    elif 24 < minutes < 36:
      output = output.replace('1 hour and ', '1 and a half hours')
      output = output.replace(' hours and ', ' and a half hours')
    else:            output = output + "{:.0f} minutes".format(minutes)
    if (hours == 12) and (accu == "low"): output = " half a day "
 
  elif minutes > 0:
    if minutes == 1: output = "1 minute"
    elif 24 < minutes < 36: output = "half an hour"
    else:            output = "{:.0f} minutes".format(minutes)
    if 24 < seconds < 36:
      output = output.replace('1 minute', '1 and a half minutes')
      output = output.replace(' minutes', ' and a half minutes')
 
  else:
    if seconds == 1: output = "1 second"
    else:            output = "{:.0f} seconds".format(seconds)
 
  return output
 
