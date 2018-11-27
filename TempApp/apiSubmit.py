#!/usr/bin/env python
import sqlite3
import requests
import datetime

# Required variables
url = 'http://18.221.243.7:3000/temperature'
dbfile = '/root/TempApp/temperature.db'
table = 'temperature'
col1 = 'processed'
col2 = 'key'
processed_at = datetime.datetime.now()

# Connection the the Sqlite database
conn = sqlite3.connect(dbfile, isolation_level=None)
c = conn.cursor()

# Query to pull the most recently created record
c.execute('SELECT device_name, temp_in_f, temp_in_c, percent_humidity, created_at FROM {tn} WHERE {cl} = 0 ORDER BY created_at DESC' .\
	format(tn=table,cl=col1))
conn.commit()

# Variables set from the SQL Select statement, uncomment the print lines to show the value for troubleshooting
one_row = c.fetchone()
#print(one_row)
device_name = one_row[0]
#print(device_name)
temp_in_f = one_row[1]
#print(temp_in_f)
temp_in_c = one_row[2]
#print(temp_in_c)
percent_humidity = one_row[3]
#print(percent_humidity)
source_createts = one_row[4]
#print(source_createts)

# API Payload and POST variables
payload= {'device': device_name, 'temp_in_f': temp_in_f, 'temp_in_c': temp_in_c,'humidity': percent_humidity,'sourcecreatets': source_createts,'inserted_at': processed_at, 'processed': '1', 'note': 'Python App Running on: ' + device_name}
r = requests.post(url, data=payload)

print('Sending to API')

# Submit data to API
r.text
r.status_code

print(r.status_code)
# Show the row processed
print('Row Processed):', one_row)

# Update the record pushed to the API to reflect it was processed
c.execute('UPDATE {} SET processed = ?, processed_at = ? WHERE device_name = ? AND created_at = ?' .\
	format(table), (1,processed_at,device_name,source_createts))
conn.commit()
print('Record successfully processed')

# Close the database connection
conn.close()
