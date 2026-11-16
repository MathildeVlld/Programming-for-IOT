import json
import cherrypy
import requests


class BikeManager:
    def orderSlots(self, stations, order="descend", N=10):
        reverse_order = (order == "descend")
        sorted_stations = sorted(
            stations, key=lambda station: station["slots"],
            reverse=reverse_order
        )
        return {"stations": sorted_stations[:N]}

    def orderBikes(self, stations, order="descend", N=10):
        reverse_order = (order == "descend")
        sorted_stations = sorted(
            stations, key=lambda station: station["bikes"],
            reverse=reverse_order
        )
        return {"stations": sorted_stations[:N]}

    def availableElectric_freeSlots(self, stations, N=10, M=5): #me renvoie rien ??
        results = []
        for station in stations:
            if station["electrical_bikes"] > N and station["slots"] > M:
                results.append(station)
        return {"stations": results}

    def countBikesAndSlots(self, stations):
        total_bikes = sum(station["bikes"] for station in stations)
        total_slots = sum(station["slots"] for station in stations)
        return {"Available Bikes": total_bikes, "Free slots": total_slots}


class MyBikeREST:
    exposed = True

    def __init__(self):
        with open("config.json", "r") as f:
            config = json.load(f)
        self.bike_url = config.get(
            "bikeURL", "https://www.bicing.barcelona/en/get-stations"
        )
        self.bike_manager = BikeManager()

    def GET(self, *uri, **params):
        if len(uri) == 0:
            return json.dumps({"message": "Welcome to the Bike REST API"})

        endpoint = uri[0]
        available = ["orderSlots", "orderBikes",
                     "availableElectric_freeSlots", "countBikesAndSlots"]
        if len(uri) != 1 or endpoint not in available:
            raise cherrypy.HTTPError(404, "Endpoint not found")

        try:
            N = int(params.get("N", 10))
            M = int(params.get("M", 5))
        except ValueError:
            raise cherrypy.HTTPError(400, "N and M must be integers")

        if N < 0 or M < 0:
            raise cherrypy.HTTPError(400, "N and M cannot be negative")

        order = params.get("order", "descend")
        if order not in ["ascend", "descend"]:
            raise cherrypy.HTTPError(400, "order must be ascend or descend")

        try:
            response = requests.get(self.bike_url, timeout=15)
            response.raise_for_status()
            data = response.json()
            stations = data["stations"]
        except (requests.RequestException, ValueError, KeyError):
            raise cherrypy.HTTPError(502, "Could not retrieve bike station data")

        if endpoint == "orderSlots":
            result = self.bike_manager.orderSlots(stations, order, N)
        elif endpoint == "orderBikes":
            result = self.bike_manager.orderBikes(stations, order, N)
        elif endpoint == "availableElectric_freeSlots":
            result = self.bike_manager.availableElectric_freeSlots(stations, N, M)
        else:
            result = self.bike_manager.countBikesAndSlots(stations)

        return json.dumps(result)


if __name__ == "__main__":
    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True
        }
    }
    cherrypy.tree.mount(MyBikeREST(), "/", conf)
    cherrypy.config.update({"server.socket_port": 8090})
    cherrypy.engine.start()
    cherrypy.engine.block()
