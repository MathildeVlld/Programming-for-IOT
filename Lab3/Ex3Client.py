import requests


SERVER_URL = "http://127.0.0.1:8080"


def showRules():
    response = requests.get(SERVER_URL + "/listRules", timeout=5)
    response.raise_for_status()
    rules = response.json().get("listRules", [])

    if not rules:
        print("There are no control rules.")
        return

    print("\nExisting rules:")
    for rule in rules:
        room = rule.get("roomName", "room not specified")
        print("- Room:", room,
              "| Type:", rule["rule_type"],
              "| Threshold:", rule["threshold"])


def addRule():
    room = input("Room name (e.g. living_room): ").strip()
    rule_type = input("Rule type (temperature/light): ").strip().lower()
    threshold = float(input("Threshold value: "))

    data = {
        "roomName": room,
        "rule_type": rule_type,
        "threshold": threshold
    }
    response = requests.post(
        SERVER_URL + "/addNewRule", json=data, timeout=5
    )
    response.raise_for_status()
    print(response.json().get("message", "Rule added."))


def evaluateRules():
    data = {}
    temperature = input("Current temperature (Enter to skip): ").strip()
    light = input("Current light level (Enter to skip): ").strip()

    if temperature:
        data["temperature"] = float(temperature)
    if light:
        data["light"] = float(light)

    if not data:
        print("No measurements entered.")
        return

    response = requests.post(
        SERVER_URL + "/evaluateRule", json=data, timeout=5
    )
    response.raise_for_status()
    result = response.json()
    print("\nEvaluation results:")
    for item in result.get("results", []):
        print("-", item)


def updateRule():
    rule_type = input("Rule type to update (temperature/light): ").strip().lower()
    new_threshold = float(input("New threshold: "))

    data = {"rule_type": rule_type, "new_threshold": new_threshold}
    response = requests.put(
        SERVER_URL + "/updateRule", json=data, timeout=5
    )
    response.raise_for_status()
    print(response.json().get("message", "Rule updated."))


def deleteRule():
    rule_type = input("Rule type to delete (temperature/light): ").strip().lower()
    response = requests.delete(
        SERVER_URL + "/deleteRule/" + rule_type, timeout=5
    )
    response.raise_for_status()
    print(response.json().get("message", "Rule deleted."))


def main():
    while True:
        print("\n--- Rule Controller ---")
        print("1. Show existing rules")
        print("2. Add a new rule")
        print("3. Evaluate measurements")
        print("4. Update a rule")
        print("5. Delete a rule")
        print("0. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                showRules()
            elif choice == "2":
                addRule()
            elif choice == "3":
                evaluateRules()
            elif choice == "4":
                updateRule()
            elif choice == "5":
                deleteRule()
            elif choice == "0":
                print("Goodbye.")
                break
            else:
                print("Please choose a valid option.")
        except requests.exceptions.HTTPError as error:
            print("Server error:", error)
            if error.response is not None:
                print(error.response.text)
        except requests.exceptions.RequestException as error:
            print("Connection error. Is the RuleController server running?")
            print(error)
        except ValueError:
            print("Please enter a valid number.")


if __name__ == "__main__":
    main()
