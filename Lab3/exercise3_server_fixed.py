import json
import cherrypy


class ConditionRule:
    def __init__(self, threshold, threshold_type):
        self.threshold = threshold
        self.threshold_type = threshold_type

    def evaluate(self, value):
        if self.threshold_type == "upper":
            return value > self.threshold
        if self.threshold_type == "lower":
            return value < self.threshold
        raise ValueError("Invalid threshold type")


class TemperatureRule(ConditionRule):
    def __init__(self, threshold):
        super().__init__(threshold, "upper")

    def evaluate(self, temperature):
        if super().evaluate(temperature):
            return "Temperature is high: activating cooling system"
        return "Temperature is normal"


class LightRule(ConditionRule):
    def __init__(self, threshold):
        super().__init__(threshold, "lower")

    def evaluate(self, light_level):
        if super().evaluate(light_level):
            return "Light level is low: activating lights"
        return "Light level is sufficient"


class RuleControllerWebserver:
    exposed = True

    def __init__(self):
        self.listRules = []

    def GET(self, *uri, **params):
        if uri == ("listRules",):
            output = {"listRules": []}

            for rule in self.listRules:
                output["listRules"].append({
                    "roomName": rule["roomName"],
                    "rule_type": rule["rule_type"],
                    "threshold": rule["rule_object"].threshold
                })

            return json.dumps(output)

        raise cherrypy.HTTPError(404, "Command not available")

    def POST(self, *uri, **params):
        if len(uri) != 1:
            raise cherrypy.HTTPError(404, "Command not available")

        try:
            body = json.loads(cherrypy.request.body.read())
        except (ValueError, TypeError):
            raise cherrypy.HTTPError(400, "Invalid JSON body")

        if uri[0] == "addNewRule":

            room_name = body.get("roomName")
            rule_type = body.get("rule_type")
            threshold = body.get("threshold")

            if not isinstance(room_name, str) or not room_name.strip():
                raise cherrypy.HTTPError(400, "Invalid or missing room name")

            if rule_type not in ["temperature", "light"]:
                raise cherrypy.HTTPError(400, "Invalid rule type")

            if not isinstance(threshold, (int, float)):
                raise cherrypy.HTTPError(400, "Threshold must be a number")

            if any(rule["rule_type"] == rule_type for rule in self.listRules):
                raise cherrypy.HTTPError(409, "Rule already exists")

            if rule_type == "temperature":
                rule_object = TemperatureRule(threshold)
            else:
                rule_object = LightRule(threshold)

            self.listRules.append({
                "roomName": room_name.strip(),
                "rule_type": rule_type,
                "rule_object": rule_object
            })

            return json.dumps({
                "message": rule_type + " rule added successfully"
            })

        if uri[0] == "evaluateRule":

            results = []

            for rule in self.listRules:
                rule_type = rule["rule_type"]

                if rule_type == "temperature" and "temperature" in body:
                    results.append(
                        rule["rule_object"].evaluate(body["temperature"])
                    )

                elif rule_type == "light" and "light" in body:
                    results.append(
                        rule["rule_object"].evaluate(body["light"])
                    )

            return json.dumps({"results": results})

        raise cherrypy.HTTPError(404, "Command not available")

    def PUT(self, *uri, **params):
        if uri != ("updateRule",):
            raise cherrypy.HTTPError(404, "Command not available")

        try:
            body = json.loads(cherrypy.request.body.read())
            rule_type = body["rule_type"]
            new_threshold = body["new_threshold"]

        except (ValueError, TypeError, KeyError):
            raise cherrypy.HTTPError(400, "Invalid or missing parameters")

        if rule_type not in ["temperature", "light"]:
            raise cherrypy.HTTPError(400, "Invalid rule type")

        if not isinstance(new_threshold, (int, float)):
            raise cherrypy.HTTPError(400, "Threshold must be a number")

        for rule in self.listRules:
            if rule["rule_type"] == rule_type:

                rule["rule_object"].threshold = new_threshold

                return json.dumps({
                    "message": rule_type + " rule updated successfully"
                })

        raise cherrypy.HTTPError(404, "Rule not found")

    def DELETE(self, *uri, **params):
        if len(uri) != 2 or uri[0] != "deleteRule":
            raise cherrypy.HTTPError(
                404, "Use /deleteRule/<rule_type>"
            )

        rule_type = uri[1]

        for rule in self.listRules:
            if rule["rule_type"] == rule_type:

                self.listRules.remove(rule)

                return json.dumps({
                    "message": rule_type + " rule deleted successfully"
                })

        raise cherrypy.HTTPError(404, "Rule not found")


if __name__ == "__main__":

    conf = {
        "/": {
            "request.dispatch": cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True
        }
    }

    cherrypy.tree.mount(RuleControllerWebserver(), "/", conf)

    cherrypy.config.update({
        "server.socket_port": 8080
    })

    cherrypy.engine.start()
    cherrypy.engine.block()
