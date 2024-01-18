
import ssl
import json
import time
import paho.mqtt.client as mqtt
from datetime import datetime
import thread6
import random
import os
import uuid

#import rmoteStart
#import rmoteStop
import subprocess
from pyroute2 import IPDB

#from config import Config

global flag
global flag1
global flag4

context = ssl.create_default_context()

broker_address= "b-4d9d7a54-2795-4ab2-b1e7-c40ddf1113f7-1.mq.us-east-1.amazonaws.com" # No ssl://
port = 8883
user = "ehashmq1"
password = "eHash@12mqtt34!"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {str(rc)}")

    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    client.subscribe('remote-access')


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topic = msg.topic
    print(f"data received from topic: {topic}")

    if (topic=="remote-access"):
        print("Active/Deactivate remote access")

        m_decode = str(msg.payload.decode("UTF-8", "ignore"))
        print(f"data type: {type(m_decode)}")
        print(f"data decoded: {m_decode}")

        print("Converting from Json to Object...")
        m_in = json.loads(m_decode)
        print(f"converted data type: {type(m_in)}")
        
        ID=m_in['HardWareID']
        
        print("HardwareID:")
        print(ID)
        print(type(ID))
        print("DefaultID:")
        print(defaultid)
        print(type(defaultid))
        
        if (defaultid==ID):
            print("Match for this unit:")
            
            start=m_in['object']['Access']
            if (start=='0'):
                flag=0
                os.popen('/home/pi/rmoteStop.sh')
                #flag=0
            if (start=='1'):
                os.popen('/home/pi/rmoteStart.sh')
                #os.system("python3 /home/pi/2.py")
            
            print('\n')
        else: 
            print("Not matching for this unit")
                


# The callback for when a PUBLISH message is sent to the server.
def on_publish(client, userdata, mid):
    print(f"data published with message id: {mid}")
    print('\n')

def callback(a, b):
    print('Sum = {0}'.format(a+b))

if __name__ == '__main__':
    
    command = "cat /sys/class/net/tun0/operstate"   
    f = open('/home/pi/hardwareid.txt', 'r')
    data = f.read()
    f.close()
    print(data)
    defaultid=int(data)
    ID1=defaultid
    
    state=""
    flag=0
    flag1=0
    flag4=0
    #client = mqtt.Client(str(random.randrange(7))) #create new instance
    
    client = mqtt.Client(str(uuid.uuid1()))
    #client._connect_timeout = 1.0
    
    
    client.username_pw_set(user, password=password) #set username and password
     

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.tls_set_context(context=context)
    client.connect(broker_address, port=port, keepalive=1000)

    #client.connect(host=Config.MQTT_HOST, port=Config.MQTT_PORT, keepalive=60)
    client.loop_start()

    run = True
    start = time.time()

    while run:
        
        if time.time() - start > 20:
            start = time.time()
        
            payload = json.dumps(
                {
                    "HardWareID": ID1,
                    "object": {
                        "ParameterName": "Remote",
                        "Value": "1111",
                        "AlarmID": "8888"			
                        
                        
                    }
                    
                }
            )
            
            
        # time.sleep(10)
            #if (flag==1):
            #    client.publish('remote', payload=payload, qos=1, retain=True)
    
            try:  
                output = subprocess.check_output(command, shell=True)
                output= ((output).decode('ascii'))
            
                ip = IPDB()
                state = ip.interfaces.tun0.operstate
                print(state)
                #if (state=="UNKNOWN"):
                    #client.publish('iot-data3', payload=payload, qos=1, retain=True)
                ip.release()
                flag4=0
                    

            except subprocess.CalledProcessError as e:
                state="ABC"
                flag=0
                flag1=0
                output=(e.output)
            
            
            print(output)
            
            if (state=="UNKNOWN"):
    # and flag==0):
                print ("VPN ACTIVE")
                #client.publish('iot-data3', payload=payload, qos=1, retain=True)
                flag=1
                flag2=0
                #flag4=0
            else:
                print("VPN NOT ACTIVE")
                flag2=1
            #client.publish('remote', payload=payload, qos=1, retain=True)client.publish('remote', payload=payload, qos=1, retain=True)
            if (flag==1):
                if (flag1==0):
                    print("update remote value on")
                    #f = open('/home/pi/remote.txt', 'w')
                    #f.write('2')
                    #f.write('2')
                    #f.close
                    with open('/home/pi/remote.txt', 'w') as f:
                        f.write('2')
                    flag1=1
                    #client.publish('iot-data3', payload=payload, qos=1, retain=True)
                    time.sleep(0.5)
                    print("Done")
            if (flag2==1):
                if(flag4==0):        
                    print("update remote value off")
                    #f = open('/home/pi/remote.txt', 'w')
                    #f.write('1')
                    #f.close
                    with open('/home/pi/remote.txt', 'w') as f:
                        f.write('1')
                    #time.sleep(0.5)
                    flag4=1
                    time.sleep(0.5)

                #client.publish('iot-data3', payload=payload, qos=1, retain=True)
        #time.sleep(20)

    #client.loop_stop()
    client.disconnect()








