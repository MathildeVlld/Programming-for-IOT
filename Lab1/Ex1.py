import json

class DeviceManager:
    def __init__(self):
        self.catalog=json.load(open("catalog.json"))
          
    def searchByName(self):
            user_input_name=input("Enter the desired Device Name: ")
            devices_list=self.catalog["devicesList"]
            
            devices_found=[]
            found=False
            
            for device in devices_list:
                if device["deviceName"]==user_input_name:
                    devices_found.append(device)
                    found=True
        
            if found:
                print(devices_found)
            else:
                print("No Devices found with that name")

    def searchByID(self):
        user_input_id=input("Enter the desired Device ID: ")
        devices_list=self.catalog["devicesList"]
        
        devices_found=[]
        found=False
        
        for device in devices_list:
            if device["deviceID"]==user_input_id:
                devices_found.append(device)
                found=True
    
        if found:
            print(devices_found)
        else:
            print("No Devices found with that ID")

    def searchByService(self):
        user_input_name=input("Enter the desired Device Service: ")
        devices_list=self.catalog["devicesList"]
        
        devices_found=[]
        found=False
        
        for device in devices_list:
            if device["availableServices"] and user_input_name in device["availableServices"]:
                devices_found.append(device)
                found=True
    
        if found:
            print(devices_found)
        else:
            print("No Devices found with that Service")

    def searchByMeasureType(self):
        user_input_Measure=input("Enter the desired Measure Type: ")
        devices_list=self.catalog["devicesList"]

        for device in devices_list:
            if user_input_Measure in device['measureType']:
                print(device)
                return
        print("No devices found for this measure type")
    

    def insertDevice(self):
        user_input_id=input("Enter the new Device ID: ")
        devices_list=self.catalog["devicesList"]
        found=False
        for device in devices_list:
            if device["deviceID"]==user_input_id:
                found=True
                break
        if found:
            print("The ID inserted already exists. Please check for adding a new device")
        else:
            user_input_name=input("Please enter the Device Name:")
            available_services = []
            available_measure_types = []

            while True:
                service = input("Please add the serviceName available. When finish type 'ok' ")

                if service == "ok":
                    break

                available_services.append(service)

            while True:
                measure = input("Please add the measure type available. When finish type 'ok' ")

                if measure == "ok":
                    break

                available_measure_types.append(measure)
            
            device_dict = {
                "deviceName": user_input_name,
                "deviceID": user_input_id,
                "availableServices": available_services,
                "availableMeasureTypes": available_measure_types
            }            
            self.catalog["devicesList"].append(device_dict)
            with open('catalog.json', 'w') as f:
                json.dump(self.catalog, f, indent=4)
    

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
    welcome_message="Hello, welcome to the Device Manager."
    available_actions_message="The available actions are: \n 'sName' to search by name  \n 'sID' to search by ID  \n 'sService' to search by service  \n 'sMeasureType' to search by measure type  \n 'iDevice' to insert a new device \n 'pAll' to print all devices \n 'e' exit"
    condition_iterate=True
    device_manager_instance= DeviceManager()
    print(welcome_message)
    while True:
        print(available_actions_message)
        user_input=input("\n Please enter the action to be performed: ")
        if user_input == "sName":
            device_manager_instance.searchByName()
        elif user_input == "sID":
            device_manager_instance.searchByID()
        elif user_input == "sService":
            device_manager_instance.searchByService()
        elif user_input == "sMeasureType":
            device_manager_instance.searchByMeasureType()
        elif user_input == "iDevice":
            device_manager_instance.insertDevice()
        elif user_input == "pAll":
            device_manager_instance.printAll()
        elif user_input == "e" or user_input=="exit":
            condition_iterate=False
            break




"""
file= open(self.catalogfile,'w')
data = json.load(file)
newDevice = {"deviceName": deviceName, "deviceID": deviceID, "service": service, "measureType": measureType, "lastUpdate": datetime.now().strftime("%Y-%m-%d %H:%M")}
data['devicesList'].append(newDevice)
data['lastUpdate'] = datetime.now().strftime("%Y-%m-%d %H:%M")
json.dump(data, file, indent=4)
file.close()
"""




    
