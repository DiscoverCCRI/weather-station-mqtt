import serial
import os
from datetime import datetime, timezone
import time
import binascii
import Binary
import json
import mqtt_client as mqtt

class WeatherStation:
    def __init__(self, portx, bps, timex):
        self.portx = portx  # set port name
        self.bps = bps  # set port baud rate
        self.timex = timex  # set timeout limit
        self.TemperatureRTU = bytes.fromhex('26 04 00 00 00 02 77 1C')  # Request for Air temperature
        self.HumidityRTU = bytes.fromhex('26 04 00 02 00 02 D6 DC')  # Request for Air humidity
        self.PressureRTU = bytes.fromhex('26 04 00 04 00 02 36 DD')  # Request for barometric pressure
        self.LightRTU = bytes.fromhex('26 04 00 06 00 02 97 1D')  # Request for Light intensity
        self.MinDirectionRTU = bytes.fromhex('26 04 00 08 00 02 F6 DE')  # Request for Minimum wind direction
        self.MaxDirectionRTU = bytes.fromhex('26 04 00 0A 00 02 57 1E')  # Request for Maximum wind direction
        self.AvgDirectionRTU = bytes.fromhex('26 04 00 0C 00 02 B7 1F')  # Request for Average wind direction
        self.MinSpeedRTU = bytes.fromhex('26 04 00 0E 00 02 16 DF')  # Request for Minimum wind speed
        self.MaxSpeedRTU = bytes.fromhex('26 04 00 10 00 02 76 D9')  # Request for Maximum wind speed
        self.AvgSpeedRTU = bytes.fromhex('26 04 00 12 00 02 D7 19')  # Request for Average wind speed
        self.AccRainRTU = bytes.fromhex('26 04 00 14 00 02 37 18')  # Request for Accumulated rainfall
        self.AccDurationRTU = bytes.fromhex('26 04 00 16 00 02 96 D8')  # Request for Accumulated rainfall duration
        self.RainIntensityRTU = bytes.fromhex('26 04 00 18 00 02 F7 1B')  # Request for Rain intensity
        self.MaxRainIntensityRTU = bytes.fromhex('26 04 00 1A 00 02 56 DB')  # Request for Maximum rainfall intensity
        self.HeatRTU = bytes.fromhex('26 04 00 1C 00 02 B6 DA')
        self.Dumping = bytes.fromhex('26 04 00 1E 00 02 17 1A')
        self.PM2RTU = bytes.fromhex('26 04 00 30 00 02 77 13')
        self.PM10RTU = bytes.fromhex('26 04 00 32 00 02 D6 D3')
        self.ser = serial.Serial(self.portx, self.bps, timeout=self.timex)  # initialize serial port

    def Readhex(self, rtu):
        """
        Function: Read hex value from serial port
        :param rtu: 8 bytes hex value Request sent by host
        :return: 9 bytes hex value in string format
        """
        self.ser.write(rtu)
        time.sleep(0.5)
        data_len = self.ser.inWaiting()
        if data_len:
            rec_datahex = str(binascii.b2a_hex(self.ser.read(data_len)))[2:-1]
            return rec_datahex
        else:
            print("Read Timeout!")

    def Readbin(self, rtu):
        """
        Function: Read binary value from serial port
        :param rtu: 8 bytes hex value. Request sent by host
        :return: 72 bits binary value in string format
        """
        rec_databin = Binary.tobin(self.Readhex(rtu))
        return rec_databin

    def Getdata(self, rtu):
        """
        Function: Get measurement data like humidity, light intensity, etc.
        rec_databin = big endian Data format int32. Divide the data value by 1000 to get the true measurements.
        :param rtu: 8 bytes hex value. Request sent by host.
        :return: True measurement value
        """
        if rtu == self.TemperatureRTU:
            rec_databin = self.Readbin(self.TemperatureRTU)
            data = Binary.twos(rec_databin[24:56]) / 1000
        else:
            rec_datahex = self.Readhex(rtu)
            data = int(rec_datahex[6:14], 16) / 1000
        return format(data, '.3f')

def outputToJSON(dataToAdd, fileName):
    jsonData = []
    volumeDir = '/data/'
    volumeDirExists = os.path.isdir(volumeDir)

    if volumeDirExists:
        try:
            # Open the existing file
            jsonFile = open(volumeDir+fileName, "r+")
            jsonData = json.load(jsonFile)

        except FileNotFoundError:
            print(f"[+] Creating {volumeDir+fileName}...")
            jsonFile = open(volumeDir+fileName, "w")
    
    else:
        try:
            # Open the existing file
            jsonFile = open(fileName, "r+")
            jsonData = json.load(jsonFile)
        
        except FileNotFoundError:
            print(f"[-] Volume directory {volumeDir} not found. Did you mount a volume?")
            print(f"[+] Storing output to root, creating {fileName}...")
            jsonFile = open(fileName, "w")
    
    # At this point it can be assumed that weather-station-output.json exists, so we can read from and add to it.
    print(f"[+] The following data will stored: {dataToAdd}")
    jsonData.append(dataToAdd)

    jsonFile.seek(0)
    json.dump(jsonData, jsonFile, indent=4, separators=(',',': '))
    jsonFile.truncate()
    jsonFile.close()

    
def main():
    weatherDict = {}
    client = mqtt.MQTTclient()
    w = WeatherStation("/dev/ttyUSB0", 9600, 5)
    currentDate = datetime.now().strftime("%Y%m%d")
    # Should include timestamp
    hostname = os.uname()[1]
    fileName = hostname + "-weather-station-" + currentDate + ".json"

    while True:
        #weatherDict["time"] = int(time.time() * 1000000000)
        weatherDict["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")
        weatherDict["Temperature"] = w.Getdata(w.TemperatureRTU)
        weatherDict["Humidity"] = w.Getdata(w.HumidityRTU)
        weatherDict["Pressure"] = w.Getdata(w.PressureRTU)
        weatherDict["Light Intensity"] = w.Getdata(w.LightRTU)
        weatherDict["Min Wind Direction"] = w.Getdata(w.MinDirectionRTU)
        weatherDict["Max Wind Direction"] = w.Getdata(w.MaxDirectionRTU)
        weatherDict["AVG Wind Direction"] = w.Getdata(w.AvgDirectionRTU)
        weatherDict["Min Wind Speed"] = w.Getdata(w.AvgSpeedRTU)
        weatherDict["Max Wind Speed"] = w.Getdata(w.MaxSpeedRTU)
        weatherDict["AVG Wind Speed"] = w.Getdata(w.MinSpeedRTU)
        weatherDict["Accum Rainfall"] = w.Getdata(w.AccRainRTU)
        weatherDict["Accum Rainfall Duration"] = w.Getdata(w.AccDurationRTU)
        weatherDict["Rainfall Intensity"] = w.Getdata(w.RainIntensityRTU)
        weatherDict["Max Rainfall Intensity"] = w.Getdata(w.MaxRainIntensityRTU)
        weatherDict["Heating Temperature"] = w.Getdata(w.HeatRTU)
        weatherDict["The dumping of state"] = w.Getdata(w.Dumping)
        weatherDict["PM2.5"] = w.Getdata(w.PM2RTU)
        weatherDict["PM10"] = w.Getdata(w.PM10RTU)
        pub = json.dumps(weatherDict)
        client.publish("nau-iot/weather2/seeed-weather", pub)
        outputToJSON(weatherDict, fileName)
        time.sleep(1)

if __name__ == "__main__":
    main()
        
