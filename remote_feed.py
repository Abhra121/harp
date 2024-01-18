
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

global flag3

#from config import Config

context = ssl.create_default_context()

broker_address= "b-4d9d7a54-2795-4ab2-b1e7-c40ddf1113f7-1.mq.us-east-1.amazonaws.com" # No ssl://
port = 8883
user = "ehashmq1"
password = "eHash@12mqtt34!"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {str(rc)}")

    # Subscribing in on_connect() means that if we lose the connection and reconnect then subscriptions will be renewed.
    #client.subscribe('iot-data3')


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    topic = msg.topic
    print(f"data received from topic: {topic}")

    


# The callback for when a PUBLISH message is sent to the server.
def on_publish(client, userdata, mid):
    print(f"data published with message id: {mid}")
    print('\n')


if __name__ == '__main__':

    f = open('/home/pi/hardwareid.txt', 'r')
    ID = f.read()
    f.close()
    print(ID)
    ID=int(ID)
    flag3=0
    #client = mqtt.Client()
    #client.on_connect = on_connect
    #client.on_message = on_message
    
    client = mqtt.Client(str(uuid.uuid1())) #create new instance
    #client._connect_timeout = 1.0
    
    #client = mqtt.Client("Test5") #create new instance
    client.username_pw_set(user, password=password) #set username and password
     

    #client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish
    client.tls_set_context(context=context)
    client.connect(broker_address, port=port)

    #client.connect(host=Config.MQTT_HOST, port=Config.MQTT_PORT, keepalive=60)
    client.loop_start()

    run = True
    start = time.time()

    while run:
        # publishes every 15 seconds
        #time.sleep(15)
        if time.time() - start > 20:
            start = time.time()

            f = open('/home/pi/remote.txt', 'r')
            remote = f.read()
            f.close()
            print(remote)
            #remote=int(remote)
            payload = json.dumps(
                {
                    "HardWareID": ID,
                    "object": {
                        "ParameterName": "Remote",
                        "Value": "1111",
                        "AlarmID": "8888"
                        
                        
                    }
                    
                }
            )
            if (remote=='2'):
                if (flag3==0):
                    print("update tunnel status")
                    flag3=1
                    client.publish('iot-data3', payload=payload, qos=1, retain=True)
            if (remote=='1'):
                flag3=0
        #time.sleep(20)
        
    #client.loop_stop()
    client.disconnect()









