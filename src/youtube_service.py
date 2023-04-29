import requests
import time
from mqtt_manager import mqtt_client
from secret import *

TIME_CHECK = 600
API = "https://www.googleapis.com/youtube/v3/channels?part=statistics&id={}&key={}"
YOUTUBE_ICON_ID = 10247
DEAD_API_ICON_ID = 41443
class youtube_service:

    mqtt = None
    current_subscribers = 0
    def __init__(self) -> None:
        self.init_mqtt_client()
        pass

    def request_api(self):
        result = ""
        try:
            command = self.create_request_command()
            x = requests.get(command)
            result = x.json()
        except:
            result = ""

        return result

    def create_request_command(self):
        command = API.format(CHANNEL_ID,KEY)
        return command
    

    def get_subscribers_counter(self):
        result = self.request_api()
        subscribers = 0
        if (len(result)==0):
            return
        try:
            subscribers = result['items'][0]['statistics']['subscriberCount']
        except:
            subscribers = -1
        return subscribers
    
    def create_message(self):
        counter = self.get_subscribers_counter()
        message = ""
        if (counter == -1):
            message = "Your API is dead: "
            return message,DEAD_API_ICON_ID
        
        message = "Subscribers: {}".format(counter)

        return message,YOUTUBE_ICON_ID


    def youtube_service_loop(self):
        while True:
            message,iconId = self.create_message()
            self.mqtt.send_current_subscribers(message,iconId)
            time.sleep(TIME_CHECK)


    def init_mqtt_client(self):
        self.mqtt = mqtt_client()