import json
from datetime import datetime

class Catalog:
    def __init__(self, catalogFileJSON):
        self.catalogfile=catalogFileJSON
        self.catalog=json.load(open(catalogFileJSON))

    def searchByName(self, deviceName):
        for device in self.catalog['devicesList']:
            if device['deviceName'] == deviceName:
                print(device)
                return
        print("Device not found")

    def searchByID(self, deviceID):
        for device in self.catalog['devicesList']:
            if device['deviceID'] == deviceID:
                print(device)
                return
        print("Device not found")

    def searchByService(self, service):
        for device in self.catalog['devicesList']:
            if service in device['availableServices']:
                print(device)
                return
        print("No devices found for this service")

    def searchByMeasureType(self, measureType):
        for device in self.catalog['devicesList']:
            if measureType in device['measureType']:
                print(device)
                return
        print("No devices found for this measure type")

    def insertDevice(self,deviceName,deviceID,service,measureType):
        for device in self.catalog['devicesList']:
            if device['deviceID']==deviceID:
                print("Device already present. Please update the information.")
                return
        newDevice={"deviceID":deviceID,"deviceName":deviceName,"measureType":[measureType],"availableServices":[service],"servicesDetails":[],"lastUpdate":datetime.now().strftime("%Y-%m-%d")}
        self.catalog['devicesList'].append(newDevice)

    def printAll(self):
        print(self.catalog['projectOwner'])
        print(self.catalog['projectName'])
        print(self.catalog['lastUpdate'])
        print(self.catalog['broker']['IP'])
        print(self.catalog['broker']['port'])
        for device in self.catalog['devicesList']:
            print(device)
            
    def exit(self):
        file= open(self.catalogfile,'w')
        json.dump(self.catalog, file, indent=4)
        file.close()


if __name__=="__main__":
    catalogFileJSON = "catalog.json"
    catalog1 = Catalog(catalogFileJSON)
    catalog1.searchByName("DHT11")
    catalog1.searchByID("s-001")
    catalog1.searchByService("REST")
    catalog1.searchByMeasureType("Temperature")
    catalog1.insertDevice("DHT22","s-002","REST","Temperature")
    catalog1.printAll()
    catalog1.exit()




"""
file= open(self.catalogfile,'w')
data = json.load(file)
newDevice = {"deviceName": deviceName, "deviceID": deviceID, "service": service, "measureType": measureType, "lastUpdate": datetime.now().strftime("%Y-%m-%d %H:%M")}
data['devicesList'].append(newDevice)
data['lastUpdate'] = datetime.now().strftime("%Y-%m-%d %H:%M")
json.dump(data, file, indent=4)
file.close()
"""




    
