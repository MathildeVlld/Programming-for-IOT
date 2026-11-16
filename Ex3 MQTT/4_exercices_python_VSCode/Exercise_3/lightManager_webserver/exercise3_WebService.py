import cherrypy
import os
import json
import sys
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
WEB_DIR = Path(__file__).resolve().parent
MANAGER_DIR = BASE_DIR / "lightManager"

# Import LightManager from Exercise 2
sys.path.insert(0, str(MANAGER_DIR))
from lightManager import LightManager


class LightREST(object):
    exposed = True

    def __init__(self):

        # Load configuration from lightActuator
        config_path = BASE_DIR / "lightActuator" / "config.json"

        with open(config_path, "r") as f:
            conf = json.load(f)

        broker = conf["broker"]
        port = conf["port"]

        # Topics from Exercise 2
        topic_publish = conf["topic_led_management"]
        topic_subscribe = conf["topic_led_alert"]

        # Create MQTT client using Exercise 2 LightManager
        self.light_client = LightManager(
            "IOTMQTT_REST_MANAGER_2026",
            broker,
            port,
            topic_publish,
            topic_subscribe
        )

        self.light_client.startSim()

    def GET(self):
        # Return the HTML page
        cherrypy.response.headers["Content-Type"] = "text/html"
        return (WEB_DIR / "index.html").read_bytes() #`read_bytes()` reads the HTML file as bytes so CherryPy can send it to the browser

    def PUT(self, *uri):

        # Extract command from URL: /on or /off
        if len(uri) != 1 or uri[0] not in ("on", "off"):
            raise cherrypy.HTTPError(400, "Invalid command")

        command = uri[0]

        # Publish MQTT message
        self.light_client.publish(command)

        return "Command sent: " + command


if __name__ == "__main__":

    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.staticdir.root': str(WEB_DIR)
        },

        # CSS files
        '/css': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'css'
        }
    }

    # CherryPy server configuration
    cherrypy.config.update({
        'server.socket_host': '127.0.0.1',
        'server.socket_port': 8080
    })

    # create an instance of our REST application
    app = LightREST()

    # register a function to close the MQTT connection when the server stops
    cherrypy.engine.subscribe("stop", app.light_client.stopSim)

    #start the CherryPy web server, making our application ready to handle HTTP requests
    cherrypy.quickstart(app, '/', conf)
