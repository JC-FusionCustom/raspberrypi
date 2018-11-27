#!/usr/bin/python
import sys
import sqlite3
import datetime
import socket
from datetime import datetime, timedelta

# Required variables
dbfile = '/root/TempApp/temperature.db'
table = 'temperature'
device_name = socket.gethostname()
process_ts = datetime.now()
col1 = 'device_name'
col2 = 'processed'
col3 = 'created_at'
lstwk = datetime.today() - timedelta(days=7)


# sqlite3 connection to the temperature database
conn = sqlite3.connect(dbfile, isolation_level=None)
c = conn.cursor()

# Count the number of records that will meet the cleanup criteria
# this varaible will be used in the console print out to let
# the user know how many records will be removed.
c.execute("SELECT COUNT({c1}) FROM {tn} WHERE {c2} = 1 AND {c3} < '{vl1}'" .\
        format(tn=table,c1=col1,c2=col2,c3=col3,vl1=lstwk))
conn.commit()

# Assign the row to a variable one_row
one_row = c.fetchone()

# Assign the count to a variable
record_count = one_row[0]

# Print the number of rows that will be removed as part of the cleanup
print "The number of records that will be removed is ", record_count, "total"

# Execute the delete statement to remove records that are older
# than one week and have been successfully submitted to the api
c.execute("DELETE FROM {tn} WHERE {c2} = 1 AND {c3} < '{vl1}'" .\
        format(tn=table, c2=col2,c3=col3,vl1=lstwk))
conn.commit()

# Close the database connection and notify that the script is complete
conn.close()
print('Cleanup script has successfully finished')
