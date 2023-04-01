#!/bin/bash

python3 /home/aba275/weatherMQTT/sub.py >> /home/aba275/weatherMQTT/logs/weather_sub-`date '+%Y%m%d'`.log 2>&1 
