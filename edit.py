import json

admin = {"name": "admin", "password": "admin"}


def login():
    name = input("Enter username")
    password = input("Enter password")
    if name == admin["name"] and password == admin["password"]:
        print("Admin logged.")
        return True
    else:
        print("Try again")
        return False


def editPlayer():
    players = open("Bundesliga.json")
    players = json.load(players)
    option = int(input("Find player by: 1-name 2-team"))
    if option == 1:
        name = input("Enter player's name")
        for player in players:
            if player["NAME"] == name:
                print(player)
                attribute = input("Enter the attribute which you want to edit.")
                value = int(input("Enter the new value of the attribute"))
                player[attribute.upper()] = str(value)
                with open("Bundesliga.json", "r+") as f:
                    f.seek(0)
                    f.truncate()
                    json.dump(players, f)
            # else:
            #     name = input("Player not found. Try again.")
    else:
        print("Invalid choice")
