Authors: Yiwei Zhang, NAU IoT (Duane Booher, Jacob Hagan, Akiel Aries)

# Introduction 
This repository contains sample code to read and collect Seeed SenseCAP ONE S900 Compact Weather Station data within a Docker container. The purpose of this code is to support the Discover project at Northern Arizona University.

Users may use this code as a starting point for any experiments that may utilize the Seeed SenseCAP ONE S900 Compact Weather Station.

The following steps outline the dependencies for the project and provide installation instructions to get the project running on a local device. 

# Hardware
The system that was used to host this project is a Raspberry Pi 3 Model B running Ubuntu Server 20.04, with a [Seeed SenseCAP ONE S900 Compact Weather Station](https://files.seeedstudio.com/products/101990784/SenseCAP%20ONE%20Compact%20Weather%20Sensor%20User%20Guide-v1.6.pdf) attached via USB using a [USB to RS485 Serial Port Converter Adapter Cable](https://www.amazon.com/Serial-Converter-Adapter-Supports-Windows/dp/B076WVFXN8/ref=asc_df_B076WVFXN8/?tag=hyprod-20&linkCode=df0&hvadid=309776868400&hvpos=&hvnetw=g&hvrand=15455232194279378143&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=1013406&hvtargid=pla-486428615671&th=1).

![Seeed SenseCap ONE S900](images/sensecap-one-s900.png)

*Figure 1: Seeed SenseCap ONE S900 Compact Weather Station.*

![RS-485 wiring](images/RS-485-wiring.png)

*Figure 2: Wiring demonstration for the RS-485 Serial Port Converter.*

# Software Installation process
This application is setup to run on two seperate servers/machines, one for reading and publishing the data
gathered from a Seeed SenseCAP ONE S900 Compact Weather Station over MQTT and another collecting that data
to insert into an instance of MariaDB. The collector piece also hosts an instance of grafana to visualize 
the data live.

Clone this repository:
```bash
git clone https://github.com/DiscoverCCRI/weather-station-test1.git
```

## Installing MariaDB 
```
$ sudo apt install wget
$ wget https://r.mariadb.com/downloads/mariadb_repo_setup
$ echo "ad125f01bada12a1ba2f9986a21c59d2cccbe8d584e7f55079ecbeb7f43a4da4  mariadb_repo_setup" | sha256sum -c -
$ chmod +x mariadb_repo_setup
$ sudo ./mariadb_repo_setup --mariadb-server-version="mariadb-10.6"
$ sudo apt install libmariadb3 libmariadb-dev
```
> **Note** View the latest installation information [here](https://mariadb.com/docs/skysql/connect/programming-languages/c/install/)
for the Community Server package.

## Installing grafana (this installation follows ARM-based processors)
```
# install latest version of grafana
$ sudo wget https://dl.grafana.com/enterprise/release/grafana-enterprise_9.3.1_arm64.deb
# reload systemctl daemon
$ sudo /bin/systemctl daemon-reload
# enable grafana systemctl service
$ sudo /bin/systemctl enable grafana-server
# install elements
$ sudo dpkg -i grafana-enterprise_9.3.1_arm64.deb
```
The repository also features a JSON styled grafana template to import with some example 
queries, [`grafana_template.json`](https://github.com/DiscoverCCRI/weatherMQTT/blob/main/grafana_template.json)

## Installing Python dependencies
```
# dependencies are housed within the requirements.txt file
$ pip install -r requirements.txt
```
> **Note** Be sure to setup your services for your respective servers/machines, one for the weather station publish and another for
the weather station subscribe.

## Systemd service
> **Note** It is recommended to test the `weatherMQTT/read.py` and `sub.py` scripts on their respective servers/machines
before setting them up as services to ensure data is being transmitted as expected.

Install systemd with `$ sudo apt-get install systemd`


### **MACHINE 1: Weather station PUBLISH**
This portion of the workflow requires the connection to the internet as well as a Seeed SenseCAP ONE S900
weather station node along with an installation of MQTT. Assuming these prerequisites are met, do the following:
1. move the `weather_pub.service` file to the proper location for systemd
`$ mv weather_pub.service /etc/systemd/system/`
2. edit the service file as needed, specifically the `ExecStart=` variable to point to the correct location
of the shell script that will run the `read.py` script and dump necessary outputs to logs. 
3. run `$ sudo systemctl start weather_pub.service` and check its status with `$ sudo systemctl status weather_pub.service`

### **MACHINE 2: Weather station SUBSCRIBE**
This portion of the workflow assumes that MariaDB is setup as well as MQTT. 
1. enter the MariaDB shell with `$ mariadb` on the cmd line. Create the specified database "SEEED_WEATHER" using 
`create database SEEED_WEATHER;`
2. move the `weather_sub.service` file to the proper location for systemd
`$ mv weather_sub.service /etc/systemd/system/`
3. edit the service file as needed, specifically the `ExecStart=` variable to point to the correct location
of the shell script that will run the `read.py` script and dump necessary outputs to logs. 
4. run `$ sudo systemctl start weather_sub.service` and check its status with `$ sudo systemctl status weather_sub.service`
5. check if your data is being collected properly by entering the MariaDB shell once more with `$ mariadb`. Query the data
that is being stored in the `mqtt_data` table using:
    * `USE SEEED_WEATHER;`
    * `SELECT * FROM mqtt_data;`
    
The data returned should appear in a format similar to this:

|id|time|temperature|humidity|pressure|light_intensity|min_wind_direction|max_wind_direction|avg_wind_direction|min_wind_speed|max_wind_speed|avg_wind_speed|accum_rainfall|accum_rainfall_duration|rainfall_intensity|max_rainfall_intensity|heating_temperature|dumping_of_state|pm2_5|pm10|
|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|:----|
|1|1681592735673498368|21.07|12.46|79500|370|0|0|0|0|0|0|0.2|10|0|0|21.35|0|2|2|

#### Setting up Grafana
To visualize the data populated in the database follow these loose instructions on setting up a data source and 
a dashboard for readings. View the official documentation [here](https://grafana.com/docs/grafana/latest/). 

1. When visiting `localhost:3000` in a browser login or setup your grafana user account. Edit your configuration settings
to use MySQL as a data source. 
![grafana_0](https://github.com/DiscoverCCRI/weatherMQTT/blob/main/images/grafana_0.png)

2. Edit your data source to include the database name and hostname.
![grafana_1](https://github.com/DiscoverCCRI/weatherMQTT/blob/main/images/grafana_1.png)

3. Create a dashboard of your database to start adding panels to visualize.
![grafana_2](https://github.com/DiscoverCCRI/weatherMQTT/blob/main/images/grafana_2.png)

4. Create panels for your dashboard simply with SQL queries. This example queries temperature and time
to group by the latter.
![grafana_3](https://github.com/DiscoverCCRI/weatherMQTT/blob/main/images/grafana_3.png)

Example JSON output:
```json
[
    {
        "timestamp": "1681708081446991104"
        "Temperature": "22.940",
        "Humidity": "18.560",
        "Pressure": "79310.000",
        "Light Intensity": "645.000",
        "Min Wind Direction": "0.000",
        "Max Wind Direction": "0.000",
        "AVG Wind Direction": "0.000",
        "Min Wind Speed": "0.000",
        "Max Wind Speed": "0.000",
        "AVG Wind Speed": "0.000",
        "Accum Rainfall": "0.200",
        "Accum Rainfall Duration": "10.000",
        "Rainfall Intensity": "0.000",
        "Max Rainfall Intensity": "0.000",
        "Heating Temperature": "22.780",
        "The dumping of state": "0.000",
        "PM2.5": "0.000",
        "PM10": "0.000",
    }
]
```

# Contribute
Here's a list of immediate improvements to be made:
1. Soon, we will be experimenting with Docker Compose with an MQTT container to deliver weather station updates over MQTT.
2. A lot of the functional code needs to be refactored to improve readability.
    * A note about this: There is a known read timeout error that is being worked on. A bug fix will come alongside the aforementioned refactor.

