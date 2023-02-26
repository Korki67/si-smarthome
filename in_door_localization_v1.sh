locat=$1	# index of location: 0=Wind, 1=Gate, 2=Bad1, 3=Arbeit, 4=Nord
count=$2	# number of loops to average		20
sleep=$3	# seconds to sleep between loops	40
ping=$4		# seconds for test measurement		1.0

cd /home/pi/Triangle

# copy following line into rc.local and replace <n> by the location number
# /home/pi/Triangle/hci_tri <n> 20 40 1.0 >> /home/pi/Triangle/hci_tri.log 2>&1 &

# fill-in the BT MAC addresses into the lines of the file 'MAC'
# the first line is the mobile no 1, 2nd is 2 and so forth
# format: xx:xx:xx:xx:xx:xx

##################
# signal available
##################
sig_avail() {
  i=0
  valid=0
  c=$( printf "%x" $2 )	# convert to hex for groupwrite
  while [ "$i" -lt "3" ]; do
    hcitool cc $1 > /dev/null 2>&1
    if [ $? -eq 0 ]; then
      x=`hcitool rssi $1 2>&1`
      if [ $? -eq 0 ]; then
        valid=$(( $valid + 1 ))
      fi
      i=$(( $i + 1 ))
      sleep $ping
    fi
  done
  DATE=`date '+%Y.%m.%d; %H:%M:%S'`
  if [ "$valid" -ge "2" ]; then
    echo "$DATE; $handy; Usable signal found. Start averaging signal strength."
    rssi_avrg $handy $2
    return 1
  else
    echo "$DATE; $handy; No usable signal found. Sending RSSI 99"
    h=$( printf "%x" 99 )
    groupwrite ip:192.168.22.65 3/0/10 $c $h > /dev/null
    return 0
  fi
}

##################
# RSSI average
##################
rssi_avrg() {
  i=0
  s=0
  c=$( printf "%x" $2 )	# convert to hex for groupwrite
  valid=0
  while [ "$i" -lt "$count" ]; do
    hcitool cc $1 > /dev/null 2>&1
    if [ $? -eq 0 ]; then
      x=`hcitool rssi $1 2> /dev/null`
      if [ $? -eq 0 ]; then
        valid=$(( $valid + 1 ))
        x=`echo $x | awk '{print $2}' FS=":" | sed -e s/-//`
        if [ "$x" -eq "$x" ] 2> /dev/null ; then
          s=$(( $s + $x ))
        fi
      fi
      i=$(( $i + 1 ))
      sleep 1
    fi
  done
  DATE=`date '+%Y.%m.%d; %H:%M:%S'`
  V=$(( $count / 2 ))
  if [ "$valid" -gt "$V" ]; then
    a=$(( ($s * 10 + 5) / $count / 10  ))
    h=$( printf "%x" $a )
    echo "$DATE; $handy; Average $a hex $h from $c"
    groupwrite ip:192.168.22.65 3/0/10 $c $h > /dev/null
    return 1
  else
    echo "$DATE; $handy; No usable signal found."
    return 0
  fi
}

##################
# MAIN LOOP
##################
while [ "1" -eq "1" ]; do

  hciconfig hci0 reset
  invoke-rc.d bluetooth restart

  n=1
  for i in `cat MAC`; do
    handy=$i
    code=$(( $n * 10 + $locat ))
    sig_avail $handy $code $count
    n=$(( $n + 1 ))
    sleep $sleep
  done

done
