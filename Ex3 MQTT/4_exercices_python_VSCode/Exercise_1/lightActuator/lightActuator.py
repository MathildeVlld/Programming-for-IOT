from MyMQTT import *
import time

class LightActuator:
    def __init__(self,clientID,broker,port,topic_subscribe):
        self.lightStatus = "OFF"
        self.lightClientSub = MyMQTT(clientID,broker,port,self) #self is the notifier => objectice to process the received message
        self.topic_subscribe = topic_subscribe

    def notify(self,topic,payload):  #when MyMQTT receives a message => it calls notify method 
        message_json = json.loads(payload)
        self.lightStatus = message_json["status"]
        if self.lightStatus == 1:
            print (f'The Light was turned ON at {time.ctime(message_json["timestamp"])}')
        else:
            print (f'The Light was turned OFF at {time.ctime(message_json["timestamp"])}')
            
    def startSim(self):
        self.lightClientSub.start() #connect to broker and start
        self.lightClientSub.mySubscribe(self.topic_subscribe) #passing the topic to listen 
    
    def stopSim(self):
        self.lightClientSub.unsubscribe()  #stop the connection
        self.lightClientSub.stop() #close the connection

if __name__ == "__main__":
    clientID = "IOTMQTT" #Remember that the clientID must be unique
    config = json.load(open("config.json"))
    broker = config["broker"]
    port = config["port"]
    #topic to subscribe
    topic_subscribe_lA = config["topic"]
    lightSub = LightActuator(clientID,broker,port,topic_subscribe_lA)
    lightSub.startSim()
    try:
    # Keep the main program running while Paho's background thread handles MQTT communication and incoming messages.
    # sleep(10) does NOT mean messages are checked every 10 seconds.
    # The on_message callback is triggered whenever a message arrives.
        while True: 
            time.sleep(10) #To keep the main program alive and avoid busy loop 
    except KeyboardInterrupt:
            lightSub.stopSim()