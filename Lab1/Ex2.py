class ConditionRule:
    def __init__(self, threshold):
        self.threshold = threshold

    def evaluate(self, measurement):
        raise NotImplementedError("Subclasses must implement the evaluate method.")


class LightRule(ConditionRule):
    def __init__(self, threshold):
        super().__init__(threshold)

    def evaluate(self, measurement):
        return measurement > self.threshold


class TemperatureRule(ConditionRule):
    def __init__(self, threshold):
        super().__init__(threshold)

    def evaluate(self, measurement):
        return measurement < self.threshold


class ConditionRule:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def update_rule(self, old_rule, new_rule):
        self.rules.remove(old_rule)
        self.rules.append(new_rule)

    def delete_rule(self, rule):
        self.rules.remove(rule)

    def evaluate_rules(self, measurement, rule_type):
        if rule_type == "light":
            return [rule.evaluate(measurement) for rule in self.rules if isinstance(rule, LightRule)]
        elif rule_type == "temperature":
            return [rule.evaluate(measurement) for rule in self.rules if isinstance(rule, TemperatureRule)]

if __name__ == "__main__":
    controller = ConditionRule()
    while True:
        command = input("Enter a command (add, update, delete, evaluate, rules, exit): ").strip().lower()
        if command == "add":
            rule_type = input("Enter rule type (light/temperature): ").strip().lower()
            threshold = float(input("Enter threshold value: "))
            if rule_type == "light":
                controller.add_rule(LightRule(threshold))
            elif rule_type == "temperature":
                controller.add_rule(TemperatureRule(threshold))
        elif command == "update":
            # Implement update logic here
            pass
        elif command == "delete":
            # Implement delete logic here
            pass
        elif command == "evaluate":
            rule_type = input("Enter rule type to evaluate (light/temperature): ").strip().lower()
            measurement = float(input("Enter current measurement: "))
            results = controller.evaluate_rules(measurement, rule_type)
            print(f"Evaluation results: {results}")
        elif command == "rules":
            print(f"Current rules: {controller.rules}")
        elif command == "exit":
            break
        else:
            print("Invalid command. Please try again.")