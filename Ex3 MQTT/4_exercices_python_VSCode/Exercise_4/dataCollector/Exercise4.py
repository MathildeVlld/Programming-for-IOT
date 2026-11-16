import json
import random
import time

from MyMQTT import *


class DataCollector():
    """docstring for Sensor"""

    def __init__(self, clientID, broker, baseTopic):
        self.clientID = clientID
        self.baseTopic = "IOTMQTT/"+baseTopic
        self.client = MyMQTT(clientID, broker, 1883, self)

    def run(self):
        self.client.start()
        print('{} has started'.format(self.clientID))

    def end(self):
        self.client.stop()
        print('{} has stopped'.format(self.clientID))

    def follow(self, topic):
        self.client.mySubscribe(topic)

    def notify(self, topic, msg):
        payload = json.loads(msg)
        print(json.dumps(payload, indent=4))


if __name__ == '__main__':
    conf = json.load(open("settings.json"))
    coll = DataCollector('dc'+str(random.randint(1, 10**5)), conf["broker"], baseTopic=conf["baseTopic"])
    coll.run()
    print(f'This is the client to follow the data coming from the sensors of the building of {coll.baseTopic}')
    choice = ''
    #IOTMQTT/buildingID/floorID/roomID/sensorID
    #subscribe to all measurements from the building -> <yourName>/buildingID/#
    # particular floor -> <yourName>/buildingID/floorID/#
    # particular room -> <yourName>/buildingID/floorID/roomID/#
    #example floor 2 of all buildings
    # <yourName>/+/2/#
    while choice != 'q':
        print("What kind of data you want to retrieve")
        print("\ta: data from all the building")
        print("\tf: data from a particular floor")
        print("\tr: data from a particular room")
        print("\tc: to go back to this menu")
        print("\tq: to quit")
        choice = input()
        if choice == 'q':
            break
        while choice != 'c':
            if choice == 'a': #subscribe to the entire building using /#
                coll.client.unsubscribe() # unsubscribe to remove the previous subscription. Otherwise, we might continue receiving messages from the sensors we were monitoring before
                coll.follow(coll.baseTopic+'/#') #follow to subscribe to the new topic filter
            elif choice == 'f': #ask them to enter a floor number.
                print('Type the floor [0-->4]')
                floor = str(input())
                coll.client.unsubscribe()
                coll.follow(coll.baseTopic+'/'+floor+'/#')
            elif choice == 'r': # ask them to enter both a floor and a room number
                print('Type the floor [0-->4]')
                floor = str(input())
                print('Type the room [1-->3]')
                room = str(input())
                coll.client.unsubscribe()
                coll.follow(coll.baseTopic+'/'+floor+'/'+room+'/#')
            choice = input()
        coll.client.unsubscribe()

    coll.client.unsubscribe()
    coll.end()
