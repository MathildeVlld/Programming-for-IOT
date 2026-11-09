class ConditionRule:
    def __init__(self, threshold):
        self.threshold = threshold

    def evaluate(self, value):
        return value > self.threshold

class LightRule(ConditionRule):
    def evaluate(self, light):
        return light > self.threshold

class TemperatureRule(ConditionRule):
    def evaluate(self, temperature):
        return temperature > self.threshold


class RuleController:
    def __init__(self):
        self.rules = {}

    def add(self, name, rule):
        self.rules[name] = rule

    def update(self, name, threshold):
        if name in self.rules:
            self.rules[name].threshold = threshold
            print("Rule updated.")
        else:
            print("Rule not found.")
    
    def delete(self, name):
        if name in self.rules:
            del self.rules[name]
            print("Rule deleted.")
        else:
            print("Rule not found.")

    def evaluate(self, temperature, light):
        if not self.rules:
            print("There are no rules available.")
            return

        for name, rule in self.rules.items():
            if isinstance(rule, TemperatureRule):
                result = rule.evaluate(temperature)
                print(TemperatureRule, ":", result)
                print(name, ":", result)
            elif isinstance(rule, LightRule):
                result = rule.evaluate(light)
                print(LightRule, ":", result)
                print(name, ":", result)

    def rulesList(self):
        if not self.rules:
            print("There are no rules available.")
            return

        for name, rule in self.rules.items():
            if isinstance(rule, TemperatureRule):
                print(
                    name,
                    "- Temperature - threshold:",
                    rule.threshold
                )
            elif isinstance(rule, LightRule):
                print(
                    name,
                    "- Light - threshold:",
                    rule.threshold
                )

if __name__ == "__main__":
    controller = RuleController()
    while True:
        command = input("\nEnter command (add/update/delete/evaluate/rules/exit): ")
        
        if command == "add":
            ruleType = input("Enter rule type (temperature/light): ")
            name = input("Enter rule name: ")
            threshold = float(input("Enter threshold: "))

            if ruleType == "temperature":
                rule = TemperatureRule(threshold)
                controller.add(name, rule)

            elif ruleType == "light":
                rule = LightRule(threshold)
                controller.add(name, rule)

            else:
                print("Invalid rule type.")


        elif command == "update":
            name = input("Enter rule name: ")
            threshold = float(input("Enter new threshold: "))
            controller.update(name, threshold)

        elif command == "delete":
            name = input("Enter rule name: ")
            controller.delete(name)

        elif command == "evaluate":
            temperature = float(input("Enter current temperature: "))
            light = float(input("Enter current light level: "))
            controller.evaluate(
                temperature,
                light
            )

        elif command == "rules":
            controller.rulesList()

        elif command == "exit":
            break

        else:
            print("Invalid command.")