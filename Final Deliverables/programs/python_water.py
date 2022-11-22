import random
import ibmiotf.application 
import ibmiotf.device 
from time import sleep 
import sys
organization = "nkmios" 
deviceType = "thiyagu_1" 
deviceId = "6382894739" 
authMethod = "token" 
authToken = "Yf7itNpC@hSU2naWmA"
def myCommandCallback(cmd):
    print("Command received: %s" % cmd.data['command']) 
    print(cmd)
try: 
 deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
 deviceCli = ibmiotf.device.Client(deviceOptions) 
except Exception as e: 
    print("Caught exception connecting device: %s" % str(e)) 
    sys.exit() 
#Connecting to IBM watson. 
deviceCli.connect()
while True: 
#Getting values from sensors. 
    temp_sensor =  random.randint(0,80)
    
    moist_level = random.randint(0,100)
    humidity_level = random.randint(0,30)
    
    temp_data = { 'Temperature' : temp_sensor } 
    
    moist_data = { 'Moisture Level' : moist_level} 
    humidity_data = { 'Humidity level' : humidity_level} 
    success = deviceCli.publishEvent("Temperature sensor", "json", temp_data, qos=0) 
    sleep(1)
    if success :
        print (" ............................publish ok............................. ") 
        print ("Published Temperature = %s C" % temp_sensor, "to IBM Watson") 
    if success: 
        print ("Published Moisture Level = %s " % moist_level, "to IBM Watson") 
 
    success = deviceCli.publishEvent("moist_level", "json", moist_data, qos=0) 
    sleep(1) 
    if not success: 
         print ("Published moist Level = %s cm" % moist_level, "to IBM Watson") 
         print ("")  #To send alert message if Moisture level is LOW and to Turn ON Motor-1 for irrigation. 
         if (moist_level <30): 
           print("Motor-1 is ON")
           success = deviceCli.publishEvent("Alert5", "json", { 'alert5' : "Moisture level(%s) is low Irrigation started" %moist_level }, qos=0) 
           sleep(1) 
           if not success: 
            print('Published alert5 : ' , "Moisture level(%s) is low, Irrigation started" %moist_level,"to IBM Watson" ) 
            print("") 
         else: 
            print("Motor-1 is OFF") 
            print("") 

 #command recived by farmer 
    deviceCli.commandCallback = myCommandCallback 
# Disconnect the device and application from the cloud 
    deviceCli.disconnect()
