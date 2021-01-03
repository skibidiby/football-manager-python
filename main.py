import game


def interaction(message, choices_num):
    choice = input(message)
    while not choice.isdigit():
        choice = input("Error. Please input an number: ")
    choice = int(choice)
    if choice > choices_num or choice <= 0:
        choice = input("Error. Please input valid number: ")
    else:
        return choice


while True:
    choice = interaction(
        "Welcome to Football Manager. Type 1 to enter the game or type 2 to edit the database.",
        2,
    )
    if choice == 1:
        choice = int(interaction("Press 1 to login or 2 to create a new account", 2))
        if choice == 1:
            currentManager = game.logIn()
            while True:
                choice = interaction(
                    "1 - select your starting lineup, 2 - check the current standing, 3 - proceed to the next game",
                    3,
                )
                if choice == 1:
                    players = game.playersFromTeam(game.getTeam(currentManager))
                    game.printPlayers(game.getTeam(currentManager))
                    lineup = game.chooseLineup(squad=players[0])
                elif choice == 2:
                    game.printStanding()
                elif choice == 3:
                    game.nextGame(
                        currentManager["matchday"], currentManager["team"], lineup
                    )
