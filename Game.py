class Game(object):

    def __init__(self, team1, odds1, team2, odds2):
        # ensure that the teams are in alphabetical order
        if team1 > team2:
            temp = team1
            team1 = team2
            team2 = temp
            temp = odds1
            odds1 = odds2
            odds2 = temp
        # create a unique identifier for the game
        self.name = team1 + " vs " + team2

        #store game data
        self.team1 = team1
        self.team2 = team2
        self.odds1 = odds1
        self.odds2 = odds2

    def checkForArbitrage(self, otherGame):
        # check that they are the same game
        if not (self.name == otherGame.name):
            return False

        # Figure out which team has positive odds and negative odds
        # compare for arbitrage based on that
        if self.odds1 < 0 and self.odds2 > 0:
            # check for the case that the other game has both negative odds
            if otherGame.odds2 <= 0:
                return False
            # check for arb based on whether the positive odds for one game are bigger than negative for the other
            return self.odds2 > -(otherGame.odds1) or otherGame.odds2 > -(self.odds1)
        if self.odds1 > 0 and self.odds2 < 0:
            # check for the case that the other game has both negative odds
            if otherGame.odds1 <= 0:
                return False
            # check for arb based on whether the positive odds for one game are bigger than negative for the other
            return -self.odds2 < (otherGame.odds1) or -otherGame.odds2 < (self.odds1)
        return False

    def __str__(self):
        return (self.name+": " + str(self.odds1) + " " + str(self.odds2))