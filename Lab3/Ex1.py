import json
import cherrypy
from datetime import datetime


class CatalogManager:
    def __init__(self):
        with open("catalog.json", "r") as f:
            self.catalog = json.load(f)

    def saveCatalog(self):
        with open("catalog.json", "w") as f:
            json.dump(self.catalog, f, indent=4)

    def updateDate(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.catalog["lastUpdate"] = now
        return now

    def searchByName(self, deviceName):
        results = [d for d in self.catalog["devicesList"]
                   if d["deviceName"] == deviceName]
        return {"deviceName": deviceName, "results": results}

    def searchByID(self, deviceID):
        results = [d for d in self.catalog["devicesList"]
                   if d["deviceID"] == deviceID]
        return {"deviceID": deviceID, "results": results}

    def searchByService(self, serviceType):
        results = [d for d in self.catalog["devicesList"]
                   if serviceType in d["availableServices"]]
        return {"serviceType": serviceType, "results": results}

    def searchByMeasureType(self, measureType):
        results = [d for d in self.catalog["devicesList"]
                   if measureType in d["measureType"]]
        return {"measureType": measureType, "results": results}

    def insertDevice(self, deviceInfo):
        for device in self.catalog["devicesList"]:
            if device["deviceID"] == deviceInfo["deviceID"]:
                return False

        deviceInfo["lastUpdate"] = self.updateDate()
        self.catalog["devicesList"].append(deviceInfo)
        self.saveCatalog()
        return True

    def updateDevice(self, deviceInfo):
        for i, device in enumerate(self.catalog["devicesList"]):
            if device["deviceID"] == deviceInfo["deviceID"]:
                deviceInfo["lastUpdate"] = self.updateDate()
                self.catalog["devicesList"][i] = deviceInfo
                self.saveCatalog()
                return True
        return False

    def printAll(self):
        return self.catalog


class RESTCatalog:
    exposed = True

    def __init__(self):
        self.catalogManager = CatalogManager()

    def GET(self, *uri, **params):
        if len(uri) != 1:
            raise cherrypy.HTTPError(404, "Endpoint not found")

        endpoint = uri[0]
        if endpoint == "searchByName": # http://127.0.0.1:8080/searchByName?deviceName=TestE
            if "deviceName" not in params:
                raise cherrypy.HTTPError(400, "deviceName parameter is missing")
            result = self.catalogManager.searchByName(params["deviceName"])
        elif endpoint == "searchByID":
            if "deviceID" not in params:
                raise cherrypy.HTTPError(400, "deviceID parameter is missing")
            try:
                result = self.catalogManager.searchByID(int(params["deviceID"]))
            except ValueError:
                raise cherrypy.HTTPError(400, "deviceID must be an integer")
        elif endpoint == "searchByService":
            if "serviceType" not in params:
                raise cherrypy.HTTPError(400, "serviceType parameter is missing")
            result = self.catalogManager.searchByService(params["serviceType"])
        elif endpoint == "searchByMeasureType":
            if "measureType" not in params:
                raise cherrypy.HTTPError(400, "measureType parameter is missing")
            result = self.catalogManager.searchByMeasureType(params["measureType"])
        elif endpoint == "printAll":
            result = self.catalogManager.printAll()
        else:
            raise cherrypy.HTTPError(404, "Unknown endpoint")

        return json.dumps(result)

    def POST(self, *uri, **params):
        if uri != ("insertDevice",):
            raise cherrypy.HTTPError(404, "Unknown endpoint")

        try:
            body = json.loads(cherrypy.request.body.read())
            deviceInfo = body["deviceInfo"]
            required = ["deviceID", "deviceName", "measureType",  # join the json -> with the deviceInfo encapsulation
                        "availableServices", "servicesDetails"]
            for key in required:
                if key not in deviceInfo:
                    raise ValueError("Missing field: " + key)
        except (ValueError, TypeError, KeyError):
            raise cherrypy.HTTPError(400, "Invalid JSON or device information")

        if self.catalogManager.insertDevice(deviceInfo):
            return json.dumps({"status": "Device inserted successfully"})
        raise cherrypy.HTTPError(409, "Device ID already exists. Use PUT /updateDevice to update it")

    def PUT(self, *uri, **params):
        if uri != ("updateDevice",):
            raise cherrypy.HTTPError(404, "Unknown endpoint")

        try:
            body = json.loads(cherrypy.request.body.read())
            deviceInfo = body["deviceInfo"]
            required = ["deviceID", "deviceName", "measureType",
                        "availableServices", "servicesDetails"]
            for key in required:
                if key not in deviceInfo:
                    raise ValueError("Missing field: " + key)
        except (ValueError, TypeError, KeyError):
            raise cherrypy.HTTPError(400, "Invalid JSON or device information")

        if self.catalogManager.updateDevice(deviceInfo):
            return json.dumps({"status": "Device updated successfully"})
        raise cherrypy.HTTPError(404, "Device ID not found") # on peut pas modif l'ID car c'est l'ID unique qui permet de le retrouver

    def DELETE(self, *uri, **params):
        raise cherrypy.HTTPError(405, "DELETE is not required by Exercise 1")


if __name__ == "__main__":
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True
        }
    }
    cherrypy.tree.mount(RESTCatalog(), "/", conf)
    cherrypy.config.update({"server.socket_port": 8080})
    cherrypy.engine.start()
    cherrypy.engine.block()
