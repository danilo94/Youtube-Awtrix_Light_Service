import paho.mqtt.client as mqtt
from secret import *

class mqtt_client:
    sp_client = None
    client = None
    def __init__(self) -> None:
        self.connect()

    def send_current_subscribers(self,number,iconId):
        message = '{ "duration": 10, "text":"'+number+'", rainbow:false ,"icon": '+str(iconId)+' }'
        self.client.publish(TOPIC,message)

    def reconnect(self):
        self.client.disconnect()

    def connect(self):
        self.client = mqtt.Client()
        self.client.username_pw_set(USERNAME,PASSWORD)
        self.client.connect(HOST)
        self.client.loop_start()