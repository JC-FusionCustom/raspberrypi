#!/usr/bin/env python
import sqlite3
import requests
import datetime
import time

# Required variables
url = 'http://18.221.243.7:3000/temperature'
dbfile = '/root/TempApp/temperature.db'
table = 'temperature'
col1 = 'processed'
processed_at = datetime.datetime.now()

# Sqlite connection
conn = sqlite3.connect(dbfile, isolation_level=None)
c = conn.cursor()

# Sqlite query to select records that have yet to be updated
c.execute('SELECT device_name, temp_in_f, temp_in_c, percent_humidity, created_at FROM {tn} WHERE {cl} = 0' .\
	format(tn=table,cl=col1))
conn.commit()

# Only return one row
one_row = c.fetchone()
       #print(one_row)

# Looping while statement that will run if a record is returned from the query above, else end the script
while one_row is not None:

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
		
	   # API Post payload
       payload= {'device': device_name, 'temp_in_f': temp_in_f, 'temp_in_c': temp_in_c,'humidity': percent_humidity,'sourcecreatets': source_createts,'inserted_at': processed_at, 'processed': '1', 'note': 'Python App Running on: ' + device_name} 
	   
	   # API Post request
       r = requests.post(url, data=payload)

       print('Sending to API')
	   
	   # Execute API call
       r.text
       r.status_code

       print('Row processed):', one_row)

	   # Update the record that was sent to the API
       c.execute('UPDATE {} SET processed = ?, processed_at = ? WHERE device_name = ? AND created_at = ?' .\
        	format(table), (1,processed_at,device_name,source_createts))
       conn.commit()
       print('Record successfully processed')
       time.sleep(5)
       
	   # Sqlite query to see if any additional records exist that have not been sent to the API
       c.execute('SELECT device_name, temp_in_f, temp_in_c, percent_humidity, created_at FROM {tn} WHERE {cl} = 0' .\
       		format(tn=table,cl=col1))
       conn.commit()
       
	   # Reassign the one_row variable if a value is returned, the while statement will continue to loop until the value is None(NULL)
       one_row = c.fetchone()
       #print(one_row)

else:
	# Close the Sqlite connection
       print('All caught up!')
       conn.close()
