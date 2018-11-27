# raspberrypi
Individual raspberry pi projects with Zero W / GPIO
1.	Course Goal
1.1.	Exposure to a Linux based OS
1.2.	Sensor interaction
1.3.	Data storage options
1.4.	API integration/interaction
1.5.	Python scripting
1.6.	Create IoT device with consumable data points
2.	Course Material/Items
2.1.	PI Zero W
2.2.	Jessie Lite (Linux OS)
2.3.	DHT11 Sensor
2.4.	8GB MicroSD card
2.5.	Female to Male wire harness
2.6.	Solderless GPIO headers
2.7.	Wall charger
2.8.	Micro USB cord
2.9.	PI Zero case
3.	Connect to PI Console
3.1.	Install Bonjour and connect the pi to your pc via the USB port
3.1.1.	 Link to install Bonjour 
3.2.	SSH steps to connect over WiFi(<IP Address>:22) pi:raspberry
3.3.	SSH steps to connect over Ethernet Emulator (raspberrypi.local:22) pi:raspberry
3.4.	Once connected to device, rename device using ‘sudo raspi-config’ > Hostname
3.5.	Update the device password for the pi user using ‘sudo raspi-config’
3.6.	Update the Ubuntu packages ‘apt-get update’
4.	Required Software
4.1.	Install Sqlite3 apt-get install sqlite3
4.2.	Install Python Legacy apt-get install python (Will already be installed)
The following steps will be used to install the required packages and establish the project folder:

1.	Install python-pip
apt-get install python-pip
2.	Install python gpio package
easy_install gpio
easy_install requests
3.	Enable GPIO
apt-get install rpi.gpio
raspi-config -> Interfacing Options -> Enable I2C
raspi-config -> Interfacing Options -> Enable SPI
4.	Install git
apt-get install git
5.	Install python dev tools and ssh
sudo apt-get install build-essential python-dev python-openssl
6.	Make new project directory in root
cd /root
mkdir TempApp
7.	Change to TempApp directory
cd TempApp
8.	Get git Adafruit Repo
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
9.	Change to Adafruit folder
cd Adafruit_Python_DHT
10.	Run the setup to install the module
python setup.py install

5.	Read from the sensor
5.1.	Reference the GPIO pin layout:
 

5.2.	Highlight the difference between the 3.3v and 5v (Arduino/PI)
5.3.	GPIO pins that will be used for the task 3.3v, GND, and pin 4 on right
5.4.	Create a new .py file to write the read script in /root/TempApp/
5.5.	In the Adafruit folder open the example Adafruit_Python_DHT/examples/AdafruitDHT.py. This file provides an outline on how to interact with the DHT11 sensor.
5.6.	sensorRead.py is the completed script for this step
6.	Create the local storage database
6.1.	Within the project folder, create a new sqlite3 database
6.2.	sqlite3 temperature.db
6.3.	Create the temperature table to store the data from the sensor:In
CREATE TABLE temperature(
device_name TEXT,
temp_in_f TEXT,
temp_in_c TEXT,
percent_humidity TEXT,
processed BOOLEAN,
processed_at DATE,
created_at DATE);
6.4 Insert a test record into the newly created table.
6.5 Select the test record, then remove the test record.
6.6 To see table structure use .schema to view the table.
6.7 To exit type .exit
7.	Store Reading in Sqlite3 temperature table - writeRecord.py
7.1.	Return to the .py script that we created in step 5
7.2.	Alter the script to insert the value into the Sqlite3 temperature table
7.2.1.	 The requirement for this step is to populate all table values
Device Name is the Host Name of the device
None is the equivalent of NULL
Add the insert statement to the ‘if’ portion of the script
Reference the writeRecord.py file for the desired outcome
7.3.	Upon a successful run, verify the data in the sqlite3 temperature table
7.3.1.	 sqlite3 temperature.db
8.	Restful API Interaction – apiSubmit.py
8.1.	In the project folder, create a new .py file used to submit the API post request
8.2.	Read the most recently created record in the temperature database
8.2.1.	 Reference apiSubmit.py line 20
8.2.2.	 Select the first row returned from the query
8.3.	Apply the values as variables to be used in the API POST
8.3.1.	 The URL that will be used is:
 http://ec2-13-58-115-247.us-east-2.compute.amazonaws.com:3000/temperature
8.3.2.	 Reference the apiSubmit.py file for the payload format and how to execute the post request using the requests package.
8.4.	After the API call has been made and  
8.5.	Check the MongoDB for the inserted record using the ‘device’=’device_name’ and ‘sourcecreatets’=’created_at’
8.6.	MongoDB connection information
8.6.1.	 http://ec2-13-58-115-247.us-east-2.compute.amazonaws.com:27017 dscapiuser@bdtemp | Datasource2017!
9.	Catch up script – catchupScript.py
9.1.	Create a script that will process records that were not successfully submitted to the API
9.2.	Copy the apiSubmit.py script and rename it (catcupScrip.py)
9.3.	We will add a while statement to create a loop that will identify records that need to be resent
9.3.1.	 We will continue to reassign the one_row variable until it None(NULL)
9.4.	To test the script execute the writeRecord.py script multiple times then execute catchupScript.py
10.	Scheduling Prep – tempApp.py
10.1.	To allow the scripts to run in order without having multiple cronjobs, we will trigger them from the writeRecord.py script
10.2.	Import the package subprocess
10.3.	Add the subprocess line to the if statement to be kicked off after the record is inserted into the Sqlite temperature table.
10.4.	Reference the tempApp.py file for formatting and placement
11.	Schedule the tempApp
11.1.	Open crontab using crontab -e
11.1.1.	Option 2 for Nano editor
11.2.	Add the following line: * * * * * python /root/TempApp/tempApp.py &
11.3.	Job will execute the scripts every minute while the system is on
12.	Conclusion
12.1.	We have successfully created a device that will submit temperature/humidity data every minute to a cloud data platform. This data can be accessed at any time by using the url from 8.3.1. This URL can be imported into BI tools like Microstrategy Desktop and Power BI as a data source.
