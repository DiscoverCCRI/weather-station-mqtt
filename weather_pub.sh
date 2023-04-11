#!/bin/bash

python3 /home/aba275/weatherMQTT/mqtt-test/read.py >> /home/aba275/weatherMQTT/logs/weather_pub-`date '+%Y%m%d'`.log 2>&1 
