import serial 

"""
Function: Find available serial port
"""
import serial.tools.list_ports
port_list = list(serial.tools.list_ports.comports())
print(port_list)
if len(port_list) == 0:
   print("No Serial Port Available")
else:
    for i in range(0,len(port_list)):
        print(port_list[i])
