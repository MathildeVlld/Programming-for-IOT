import json

class Sensor:
    def __init__(self,sensorName,sensorID,sensorYear,isCalibrated):
        self.sensorName=sensorName
        self.sensorID=sensorID
        self.sensorYearFabrication=sensorYear
        self.sensorCalibration=isCalibrated
    def show_sensorID(self):
        print(f"Sensor ID: {self.sensorID}, Sensor Name: {self.sensorName}")

    def current_age(self,currentYear):
        age=currentYear-self.sensorYearFabrication
        print(f"Sensor Age: {age} years")

    def is_calibrated(self):
        if self.sensorCalibration:
            print("The sensor is calibrated.")
        else:
            print("The sensor is not calibrated.")

    def read_measurements(self):
        fileContent= open('sensor1Measurements.txt').read()
        sensor1MeasurementList=fileContent.split(',')
        for i in range(len(sensor1MeasurementList)):
            sensor1MeasurementList[i]=float(sensor1MeasurementList[i])
        return sensor1MeasurementList

    def calculations(self):
        sensor1MeasurementList=self.read_measurements()
        print(f"Sensor measurements: {sensor1MeasurementList}")
        print(f"Average of the measurements: {sum(sensor1MeasurementList)/len(sensor1MeasurementList)}")
        print(f"Maximum of the measurements: {max(sensor1MeasurementList)}")
        print(f"Minimum of the measurements: {min(sensor1MeasurementList)}")

    def dico_attributes(self):
        sensor1MeasurementList=self.read_measurements()
        sensor1Dico={'Sensor Name':self.sensorName,'Sensor ID':self.sensorID,'Year of fabrication':self.sensorYearFabrication,'Is the sensor calibrated?':self.sensorCalibration,'Sensor measurements':sensor1MeasurementList}
        return sensor1Dico


if __name__=="__main__":

    sensorName=str(input('Please write the sensor name:'))
    sensorID=int(input('Please write the sensor ID:'))
    yearFabrication=int(input('Please write the year of fabrication:'))
    isCalibrated=bool(input('Is the sensor calibrated? (True/False):'))
    sensor1= Sensor(sensorName,sensorID,yearFabrication,isCalibrated)

    sensor1.show_sensorID()
    currentYear=int(input('Please write the current year:'))
    sensor1.current_age(currentYear)
    sensor1.is_calibrated()

    f=open('Info.txt','w') # or 'a' for append mode, nothing for reading mode
    # NB: ca ecrase le contenu du fichier a chaque fois qu'on lance le programme
    f.write('Sensor Name: '+sensorName+'\n' + 'Sensor ID: '+str(sensorID)+'\n'+'Year of fabrication: '+str(yearFabrication)+'\n'+'Current Year: '+str(currentYear)+'\n'+'Sensor Age: '+str(currentYear-yearFabrication)+' years'+'\n' + 'Is the sensor calibrated? '+str(isCalibrated))
    f.close()

    file = open('Info.json','w')
    json.dump(sensor1.dico_attributes(),file)
    file.close()



"""
NB :
list.remove(x) : Remove the first item from the list whose value is x. An error will occur in case there is no such item
list.pop(index) :Remove the item at the given position in the list and returns it. If no index is specified, a.pop() removes and returns the last item in the list
list.index(x) : Return the index in the list of the first item whose value is x. It is an error if there is no such item.
list.count(x) : Return the number of times x appears in the list.
list.insert(i,x) : Insert an item at a given position. The first argument is the index of the element before which to insert

JSON:
json.load(fp) : the output is a dico filled with the content of the file pointer fp (="open('file.json')")
json.dump(obj,fp) : write the dico on the fp 
json.loads(myString) : return the dico obtained by converting the string myString 
json.dumps(myDico) : return the string obtained by converting the dico myDico
"""