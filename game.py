import json
import random
import os

file = open("Bundesliga.json")
bundesliga_db = json.load(file)


class Manager:
    def __init__(self, name, team, password, matchday):
        self.name = name
        self.team = team
        self.password = password
        self.matchday = matchday

    def managerInfo(self):
        print("Hello, ", str(self.name), " you are managing", self.team)

    def saveData(self):
        data = []
        file = open("manager.json")
        file = json.load(file)
        # print(file)
        new_manager = {
            "name": self.name,
            "team": self.team,
            "password": self.password,
            "matchday": self.matchday,
        }
        if not new_manager in file:
            data.append(new_manager)
            data.extend(file)
        else:
            data.extend(file)
        with open("manager.json", "w") as outfile:
            json.dump(data, outfile)


class Fixture(object):
    def __init__(self, home, away):
        self.home = home
        self.away = away

    def generateFixtures(self):
        if len(teams) % 2:
            teams.append("Day off")
        n = len(teams)
        matches = []
        fixtures = []
        return_matches = []
        for fixture in range(1, n):
            for i in range(n // 2):
                matches.append((teams[i], teams[n - 1 - i]))
                return_matches.append((teams[n - 1 - i], teams[i]))
            teams.insert(1, teams.pop())
            fixtures.insert(len(fixtures) // 2, matches)
            fixtures.append(return_matches)
            matches = []
            return_matches = []
        print(matches)
        with open("fixtures.json", "w") as outfile:
            json.dump(fixtures, outfile)
        file = open("fixtures.json")
        fixtures = json.load(file)
        return fixtures


squad = []
teams = []
# manager = Manager("vikic", "Borussia Dortumnd", "123123", 1)
# Manager.saveData(manager)


def findTeam():
    for i in bundesliga_db:
        if not i["CLUB"] in teams:
            teams.append(i["CLUB"])
    # print(teams)
    return teams


def logIn():
    name = input("Enter username")
    password = input("Enter password")
    file = open("manager.json")
    file = json.load(file)
    for i in range(len(file[0])):
        if name in file[i]["name"]:
            if password in file[i]["password"]:
                print("logged in")
                current_manager = file[i]
                return current_manager
            break


def getMatchday(current_manager):
    file = open("manager.json")
    file = json.load(file)
    name = current_manager["name"]
    for i in range(len(file[0])):
        if name in file[i]["name"]:
            matchday = file[i]["matchday"]
            return matchday
            break


def playersFromTeam(team):
    number = 0
    rating = 0
    players = []
    for i in bundesliga_db:
        if i["CLUB"] == team:
            number = number + 1
            players.append(i)
            # print(number, i["NAME"], i["POSITION"])
            rating = rating + int(i["RATING"])
    rating = rating / number
    players = players
    return (players, rating)
    # return rating
    # players.clear()


def printPlayers(team):
    number = 0
    for i in bundesliga_db:
        if i["CLUB"] == team:
            number = number + 1
            print(number, i["NAME"], i["POSITION"])


def getTeam(current_manager):
    file = open("manager.json")
    file = json.load(file)
    team = current_manager["team"]
    for i in range(len(file[0])):
        if team in file[i]["team"]:
            matchday = file[i]["matchday"]
            return team
            break


def chooseTeam():
    findTeam()
    team = input("Type the team you want to manage:")
    while not team in teams:
        team = input("Invalid team. Please, try again:")
    return team


def chooseLineup(squad):
    lineup = []
    rating = 0
    while True:
        choice = int(
            input("1-add players, 2-remove player, 3-display lineup, 4-save lineup")
        )
        if choice == 1:
            numbers = input("Enter players numbers seperated by comma")
            numbers = numbers.split(",")
            for number in numbers:
                if squad[int(number) - 1] in lineup:
                    print("Error. Duplicating player.")
                else:
                    lineup.append(squad[int(number) - 1])
        elif choice == 2:
            number = int(input("Enter player's number"))
            lineup.pop(number)
        elif choice == 4:
            if len(lineup) < 11:
                print("Not enough players. Add ", 11 - len(lineup), " more.")
            else:
                for i in lineup:
                    rating = rating + int(i["RATING"])
                rating = rating / 11
                print(lineup, " ", rating)
                return (lineup, rating)
                break
        else:
            print(lineup)


# def contains(list, filter):
#     for x in list:
#         if filter(x):
#             return True
#     return False


def printStanding():
    table = open("table.json")
    table = json.load(table)
    # print(json.dumps(table, sort_keys=True))
    ordered_items = sorted(table, key=lambda item: item["points"], reverse=True)
    pos = 0
    print(pos, "team name ", " points", "GD")
    for i in ordered_items:
        pos = pos + 1
        print(pos, i["team"], i["points"], i["GF"] - i["GA"])
    # print(ordered_items)


def getFieldRating(team, current_team):
    if current_team:
        players = team
    else:
        players = playersFromTeam(team)
    forwards = []
    forwards_rating = 0
    midfielders = []
    midfielders_rating = 0
    defenders = []
    defenders_rating = 0
    for player in players[0]:
        if player["FIELD"] == "FWD":
            forwards.append(player)
            forwards_rating = forwards_rating + int(player["RATING"])
        elif player["FIELD"] == "MID":
            midfielders.append(player)
            midfielders_rating = midfielders_rating + int(player["RATING"])
        elif player["FIELD"] == "DEF":
            defenders.append(player)
            defenders_rating = defenders_rating + int(player["RATING"])
    forwards_rating = forwards_rating / len(forwards)
    midfielders_rating = midfielders_rating / len(midfielders)
    defenders_rating = defenders_rating / len(defenders)

    forwards_rating = (forwards_rating + midfielders_rating) / 2
    defenders_rating = (defenders_rating + midfielders_rating) / 2
    return {
        "forwards": len(forwards),
        "forwards_rating": forwards_rating,
        "defenders": len(defenders),
        "defenders_rating": defenders_rating,
    }
    # print("fwd:", (forwards_rating+midfielders_rating)/2, "def:",(defenders_rating+midfielders_rating)/2)


def generateResult(outcome, winnerH):
    # print(outcome)
    weights = [1, 1, 1, 2, 2, 2, 2, 3, 3, 4, 5]
    index = random.choice(weights)
    outcome = abs(round(outcome))
    if outcome > 7:
        outcome = 7
    if winnerH:
        home = max(index, outcome)
        away = max(index, outcome) - min(index, outcome)
    else:
        home = max(index, outcome) - min(index, outcome)
        away = max(index, outcome)
    print(home, ":", away)
    return (home, away)


def nextGame(matchday, current_team, lineup):
    print(matchday)
    file = open("fixtures.json")
    table = open("table.json")
    fixtures = json.load(file)
    table = json.load(table)
    data = []
    for team_name in fixtures[matchday]:
        # players = playersFromTeam(team_name[0])
        if team_name[0] == current_team:
            rating_home = getFieldRating(lineup, True)
            rating_away = getFieldRating(team_name[1], False)
        elif team_name[1] == current_team:
            rating_home = getFieldRating(team_name[0], False)
            rating_away = getFieldRating(lineup, True)
        else:
            rating_home = getFieldRating(team_name[0], False)
            rating_away = getFieldRating(team_name[1], False)
        print(team_name[0], " vs ", team_name[1])
        # print("home", rating_home['forwards'], "away", rating_away['defenders'])
        ATT = (rating_home["forwards_rating"] - rating_away["defenders_rating"]) * (
            rating_home["forwards"] / rating_away["defenders"]
        )
        DEF = (rating_home["defenders_rating"] - rating_away["forwards_rating"]) * (
            rating_away["forwards"] / rating_home["defenders"]
        )
        outcome = ATT - DEF

        if outcome < -0.5:
            print("WINNER: ", team_name[0])
            result = generateResult(outcome, True)
            for t in table:
                if t["team"] == team_name[0]:
                    t["points"] = t["points"] + 3
                    t["GF"] = t["GF"] + result[0]
                    t["GA"] = t["GA"] + result[1]
                if t["team"] == team_name[1]:
                    t["GA"] = t["GA"] + result[0]
                    t["GF"] = t["GF"] + result[1]
        elif outcome > 0.5:
            print("WINNER: ", team_name[1])
            result = generateResult(outcome, False)
            for t in table:
                if t["team"] == team_name[1]:
                    t["points"] = t["points"] + 3
                    t["GF"] = t["GF"] + result[1]
                    t["GA"] = t["GA"] + result[0]
                if t["team"] == team_name[0]:
                    t["GF"] = t["GF"] + result[0]
                    t["GA"] = t["GA"] + result[1]
        else:
            print("DRAW")
            result = generateResult(outcome, True)
            for t in table:
                if t["team"] == team_name[0]:
                    t["points"] = t["points"] + 1
                    t["GF"] = t["GF"] + result[0]
                    t["GA"] = t["GA"] + result[0]
                if t["team"] == team_name[1]:
                    t["points"] = t["points"] + 1
                    t["GF"] = t["GF"] + result[0]
                    t["GA"] = t["GA"] + result[0]
        with open("table.json", "r+") as f:
            f.seek(0)
            f.truncate()
            json.dump(table, f)
        # with open('table.json', 'w') as outfile:
        #     json.dump(data, outfile)


# team = chooseTeam()
# print(lineup)
# teams = findTeam()
# Fixture.generateFixtures(teams)
# current_manger = logIn()
# matchday = getMatchday(current_manger)
# current_team = getTeam(current_manger)
# playersFromTeam(current_team)
# chooseLineup(current_team)
# print(current_team)
# getFieldRating(team)
# pl = Squad(team).returnRating(team)
# print(pl[0])
# printStanding()
# team = chooseTeam()
# pl = playersFromTeam(team)
# lineup = chooseLineup(squad=pl[0])
# nextGame(1, team, lineup)