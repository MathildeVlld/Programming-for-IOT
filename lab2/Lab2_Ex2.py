import cherrypy
import json

class ConditionRule:
    def __init__(self, threshold, threshold_type):
        self.threshold = threshold
        self.threshold_type = threshold_type

    def evaluate(self, value):
        if self.threshold_type == "upper":
            return value > self.threshold
        elif self.threshold_type == "lower":
            return value < self.threshold
        else:
            raise ValueError("Invalid threshold type")


class TemperatureRule(ConditionRule):
    def __init__(self, threshold):
        super().__init__(threshold, "upper")

    def evaluate(self, temperature):
        if super().evaluate(temperature):
            return "Activating cooling system"
        else:
            return "Temperature is normal"


class LightRule(ConditionRule):
    def __init__(self, threshold):
        super().__init__(threshold, "lower")

    def evaluate(self, light_level):
        if super().evaluate(light_level):
            return "Activating lights"
        else:
            return "Light level is sufficient"


class RuleControllerWebserver:
    exposed = True

    def __init__(self):
        self.listRules = []

    def GET(self, *uri, **params):
        if len(uri) == 1 and uri[0] == "listRules":
            output = {"listRules": []}

            for rule in self.listRules:
                output["listRules"].append({
                    "rule_type": rule["rule_type"],
                    "threshold": rule["rule_object"].threshold
                })

            return json.dumps(output)

        else:
            raise cherrypy.HTTPError(404, "Command not found")

    def POST(self, *uri, **params):
        if len(uri) != 1:
            raise cherrypy.HTTPError(404, "Command not found")

        try:
            body = cherrypy.request.body.read()
            body = json.loads(body)
        except (ValueError, TypeError):
            raise cherrypy.HTTPError(400, "Invalid JSON body")

        if uri[0] == "addNewRule":
            rule_type = body.get("rule_type")
            threshold = body.get("threshold")

            if rule_type not in ["temperature", "light"]:
                raise cherrypy.HTTPError(400, "Invalid rule type")

            if threshold is None:
                raise cherrypy.HTTPError(400, "Missing threshold")

            for rule in self.listRules:
                if rule["rule_type"] == rule_type:
                    raise cherrypy.HTTPError(409, "Rule already exists")

            if rule_type == "temperature":
                rule_object = TemperatureRule(threshold)
            else:
                rule_object = LightRule(threshold)

            new_rule = {
                "rule_type": rule_type,
                "rule_object": rule_object
            }

            self.listRules.append(new_rule)

            output = {
                "input": body,
                "command": "addNewRule",
                "result": "Rule added successfully"
            }

            return json.dumps(output)

        elif uri[0] == "evaluateRule":
            results = {}

            for rule in self.listRules:
                if rule["rule_type"] == "temperature":
                    if "temperature" in body:
                        results["temperature"] = (
                            rule["rule_object"].evaluate(
                                body["temperature"]
                            )
                        )

                elif rule["rule_type"] == "light":
                    if "light" in body:
                        results["light"] = (
                            rule["rule_object"].evaluate(body["light"])
                        )

            output = {
                "input": body,
                "command": "evaluateRule",
                "result": results
            }

            return json.dumps(output)

        else:
            raise cherrypy.HTTPError(404, "Command not found")

    def PUT(self, *uri, **params):
        if len(uri) != 1 or uri[0] != "updateRule":
            raise cherrypy.HTTPError(404, "Command not found")

        try:
            body = cherrypy.request.body.read()
            body = json.loads(body)
            rule_type = body["rule_type"]
            new_threshold = body["new_threshold"]
        except (ValueError, TypeError, KeyError):
            raise cherrypy.HTTPError(400, "Invalid or missing parameters")

        if rule_type not in ["temperature", "light"]:
            raise cherrypy.HTTPError(400, "Invalid rule type")

        for rule in self.listRules:
            if rule["rule_type"] == rule_type:
                rule["rule_object"].threshold = new_threshold

                output = {
                    "input": body,
                    "command": "updateRule",
                    "result": "Rule updated successfully"
                }

                return json.dumps(output)

        raise cherrypy.HTTPError(404, "Rule not found")

    def DELETE(self, *uri, **params):
        if len(uri) != 2 or uri[0] != "deleteRule":
            raise cherrypy.HTTPError(
                400, "URL should be /deleteRule/<rule_type>"
            )

        rule_type = uri[1]

        for rule in self.listRules:
            if rule["rule_type"] == rule_type:
                self.listRules.remove(rule)

                output = {
                    "input": {"rule_type": rule_type},
                    "command": "deleteRule",
                    "result": "Rule deleted successfully"
                }

                return json.dumps(output)

        raise cherrypy.HTTPError(404, "Rule not found")


if __name__ == "__main__":
    conf = {
        "/": {
            "request.dispatch":
                cherrypy.dispatch.MethodDispatcher(),
            "tools.sessions.on": True
        }
    }

    cherrypy.tree.mount(RuleControllerWebserver(), "/", conf)
    cherrypy.config.update({"server.socket_port": 8090})
    cherrypy.engine.start()
    cherrypy.engine.block()