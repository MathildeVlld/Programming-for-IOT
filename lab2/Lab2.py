
import cherrypy
import os
import json


class DeviceRegistering:
    exposed = True #the class must be exposed, accessible from the web 

    def __init__(self):
        pass

    def GET(self, *uri, **params):
        # http://127.0.0.1:8090/ -> return index.html
        # http://127.0.0.1:8090/devicesList -> return all devices

        if len(uri) == 0:
            with open("index.html", "r") as f:
                return f.read()

        elif len(uri) == 1:
            if uri[0] == "devicesList":
                with open("devices.json", "r") as f:
                    devicesList = json.load(f)
                return json.dumps(devicesList, indent=4)
            else:
                raise cherrypy.HTTPError(404, "Command not found")
            
        else:
            raise cherrypy.HTTPError(404, "Command not found")

    def POST(self, *uri, **params):
        # Add a new device
        # URL: /addDevice

        if len(uri) == 1 and uri[0] == "addDevice":
            try:
                body_new_device = cherrypy.request.body.read()
                body_new_device = json.loads(body_new_device)

                required_fields = [
                    "deviceID",
                    "deviceName",
                    "measureType",
                    "unit"
                ]

                for field in required_fields:
                    if field not in body_new_device:
                        raise cherrypy.HTTPError(400, "Missing parameter: " + field)

            except ValueError:
                raise cherrypy.HTTPError(400, "Invalid JSON body")

            with open("devices.json", "r") as f:
                deviceDict = json.load(f)

            # Check if the deviceID already exists
            for elem_device in deviceDict["devicesList"]:
                if body_new_device["deviceID"] == elem_device["deviceID"]:
                    raise cherrypy.HTTPError(409, "Device ID already exists.")

            # Add the new device
            new_device = {
                "deviceID": body_new_device["deviceID"],
                "deviceName": body_new_device["deviceName"],
                "measureType": body_new_device["measureType"],
                "unit": body_new_device["unit"]
            }

            deviceDict["devicesList"].append(new_device)

            with open("devices.json", "w") as f:
                json.dump(deviceDict, f, indent=4)

            return json.dumps(deviceDict, indent=4)

        else:
            raise cherrypy.HTTPError(404, "POST method only expects /addDevice")

    def PUT(self, *uri, **params):
        # Update an existing device
        # URL: /updateDevice/<deviceID>

        if len(uri) == 2 and uri[0] == "updateDevice":
            device_id = uri[1]
            try:
                body_updated_device = cherrypy.request.body.read()
                body_updated_device = json.loads(body_updated_device)

                required_fields = [
                    "deviceID",
                    "deviceName",
                    "measureType",
                    "unit"
                ]

                for field in required_fields:
                    if field not in body_updated_device:
                        raise cherrypy.HTTPError(400, "Missing parameter: " + field)

            except ValueError:
                raise cherrypy.HTTPError(400, "Invalid JSON body")

            # Check that the ID in the URL matches the ID in the body
            if body_updated_device["deviceID"] != device_id:
                raise cherrypy.HTTPError(400,"DeviceID in the URI does not match the one in the body")

            with open("devices.json", "r") as f:
                deviceDict = json.load(f)

            found = False

            for elem_device in deviceDict["devicesList"]:
                if elem_device["deviceID"] == device_id:
                    found = True
                    # Update the existing device
                    elem_device.update(body_updated_device)

            if found:
                with open("devices.json", "w") as f:
                    json.dump(deviceDict, f, indent=4)
                return json.dumps(deviceDict, indent=4)

            else:
                raise cherrypy.HTTPError(404, "Device ID not found")

        else:
            raise cherrypy.HTTPError(400,"The URL should be /updateDevice/<deviceID>")

    def DELETE(self, *uri, **params):
        # Delete an existing device
        # URL: /deleteDevice/<deviceID>

        if len(uri) == 2 and uri[0] == "deleteDevice":
            device_id = uri[1]
            with open("devices.json", "r") as f:
                deviceDict = json.load(f)

            found = False
            for elem_device in deviceDict["devicesList"]:
                if elem_device["deviceID"] == device_id:
                    deviceDict["devicesList"].remove(elem_device)
                    found = True
                    break

            if found:
                with open("devices.json", "w") as f:
                    json.dump(deviceDict, f, indent=4)
                return json.dumps(deviceDict, indent=4)

            else:
                raise cherrypy.HTTPError(404, "Device ID not found")

        else:
            raise cherrypy.HTTPError(400,"The URL should be /deleteDevice/<deviceID>")


if __name__ == "__main__":
    conf = {
        "/": {
            "request.dispatch":
                cherrypy.dispatch.MethodDispatcher(),
            "tools.staticdir.root": os.path.abspath(os.getcwd()),
            "tools.sessions.on": True
        },
        "/css": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "./css"
        },
        "/js": {
            "tools.staticdir.on": True,
            "tools.staticdir.dir": "./js"
        }
    }

    cherrypy.tree.mount(DeviceRegistering(), "/", conf)
    cherrypy.config.update({"server.socket_port": 8090})
    cherrypy.engine.start()
    cherrypy.engine.block()
