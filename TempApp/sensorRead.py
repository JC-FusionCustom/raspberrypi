#!/usr/bin/python
import subprocess
import sys
import sqlite3
import Adafruit_DHT
import socket
import datetime

# Required variables
dbfile = '/root/TempApp/temperature.db'
table = 'temperature'
device_name = socket.gethostname()
process_ts = datetime.datetime.now()


# sqlite3 connection to the temperature database
conn = sqlite3.connect(dbfile, isolation_level=None)
c = conn.cursor()

# The sensor library
sensor = Adafruit_DHT.DHT11

# Provide the pi gpio pin the data wire is connected to
pin = 4

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

# Un-comment the line below to convert the temperature to Fahrenheit.
temp_in_f = str(temperature * 9/5.0 + 32)
temp_in_c = str(temperature)
hum = str(humidity)
#new_key = max_key + 1

# Note that sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).
# If this happens try again!
if humidity is not None and temperature is not None:
    print(device_name + '|' + temp_in_f + '|' + temp_in_c + '|' +  hum)
    c.execute('INSERT INTO {} VALUES (?, ?, ?, ?, ?, ?, ?)' .\
	format(table),(device_name,temp_in_f,temp_in_c,hum,0,None,process_ts))
    conn.close
    print('Sensor read and database write complete')
	# Start the API call script
    subprocess.call("/root/TempApp/apiSubmit.py", shell=True)
    print('API call complete')
	# Start the catch up script
    subprocess.call("/root/TempApp/catchupScript.py", shell=True)
    print('All caught up!')
    subprocess.call("/root/TempApp/cleanupDB.py", shell=True)
    print('Local DB has been cleaned up!')
else:
    print('Failed to get reading. Try again!')
    conn.close()
    sys.exit(1)
