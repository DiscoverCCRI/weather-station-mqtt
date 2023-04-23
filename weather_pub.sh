#!/bin/bash

python3 /home/aba275/weatherMQTT/pub/read.py >> /home/aba275/weatherMQTT/logs/weather_pub-`date '+%Y%m%d'`.log 2>&1 
