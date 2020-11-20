import json
import random
import os
file = open('Bundesliga.json')
bundesliga_db = json.load(file)


class Manager:
    def __init__(self, name, team, password, matchday):
        self.name = name
        self.team = team
        self.password = password
        self.matchday = matchday

    def managerInfo(self):
        print('Hello, ', str(self.name), ' you are managing', self.team)

    def saveData(self):
        data = []
        file = open('manager.json')
        file = json.load(file)
        # print(file)
        new_manager = {
            'name': self.name,
            'team': self.team,
            'password': self.password,
            'matchday': self.matchday
        }
        if not new_manager in file:
            data.append(new_manager)
            data.extend(file)
        else:
            data.extend(file)
        with open('manager.json', 'w') as outfile:
            json.dump(data, outfile)


class Fixture(object):
    def __init__(self, home, away):
        self.home = home
        self.away = away

    def generateFixtures(self):
        if len(teams) % 2:
            teams.append('Day off')
        n = len(teams)
        matches = []
        fixtures = []
        return_matches = []
        for fixture in range(1, n):
            for i in range(n//2):
                matches.append((teams[i], teams[n - 1 - i]))
                return_matches.append((teams[n - 1 - i], teams[i]))
            teams.insert(1, teams.pop())
            fixtures.insert(len(fixtures)//2, matches)
            fixtures.append(return_matches)
            matches = []
            return_matches = []
        print(matches)
        with open('fixtures.json', 'w') as outfile:
            json.dump(fixtures, outfile)
        file = open('fixtures.json')
        fixtures = json.load(file)
        return fixtures


lineup = []
teams = []
manager = Manager('vikic', 'Borussia Dortumnd', '123123', 1)
Manager.saveData(manager)


def findTeam():
    for i in bundesliga_db:
        if not i['CLUB'] in teams:
            teams.append(i['CLUB'])
    # print(teams)
    return teams


def logIn():
    name = input('Enter username')
    password = input('Enter password')
    file = open('manager.json')
    file = json.load(file)
    for i in range(len(file[0])):
        if name in file[i]['name']:
            if password in file[i]['password']:
                print('logged in')
                current_manager = file[i]
                return current_manager
            break


def getMatchday(current_manager):
    file = open('manager.json')
    file = json.load(file)
    name = current_manager['name']
    for i in range(len(file[0])):
        if name in file[i]['name']:
            matchday = file[i]['matchday']
            return matchday
            break


def chooseTeam():
    findTeam()
    team = input("Type the team you want to manage:")
    while not team in teams:
        team = input("Invalid team. Please, try again:")
    return team


def playersFromTeam(team):
    number = 0
    rating = 0
    players = []
    for i in bundesliga_db:
        if i['CLUB'] == team:
            number = number+1
            players.append(i)
            # print(number, ' ', i['NAME'], ' ', i['POSITION'])
            rating = rating+int(i['RATING'])
    rating = rating/number
    # return players
    return rating
    players.clear()


def chooseLineup(team):
    starting = []
    while True:
        choice = int(input("1-add player, 2-remove player, 3-display lineup"))
        if choice == 1:
            number = int(input("Enter player's number"))
            starting.append(lineup[number-1])
        elif choice == 2:
            number = int(input("Enter player's number"))
            starting.pop(number)
        else:
            print(starting)


def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False


def nextGame(matchday):
    print(matchday)
    file = open('fixtures.json')
    table = open('table.json')
    fixtures = json.load(file)
    table = json.load(table)
    data = []
    for i in fixtures[matchday]:
        # players = playersFromTeam(i[0])
        rating_home = playersFromTeam(i[0])
        rating_away = playersFromTeam(i[1])
        print(i[0], ' vs ', i[1])
        if rating_home > rating_away:
            print('WINNER: ', i[0])
            for t in table:
                if t['team'] == i[0]:
                    t['points'] = t['points']+3
        else:
            print('WINNER: ', i[1])
            for t in table:
                if t['team'] == i[1]:
                    t['points'] = t['points']+3
        with open('table.json', 'r+') as f:
            f.seek(0)
            f.truncate()
            json.dump(table, f)
        # with open('table.json', 'w') as outfile:
        #     json.dump(data, outfile)


# team = chooseTeam()
# playersFromTeam(team)
# chooseLineup(team)
# print(lineup)
# teams = findTeam()
# Fixture.generateFixtures(teams)
current_manger = logIn()
matchday = getMatchday(current_manger)
nextGame(matchday)
