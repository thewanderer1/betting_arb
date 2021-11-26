class Game(object):

    def __init__(self, team1, odds1, team2, odds2): #the url that corresponds to the sport nba/nfl/...
        if team1 > team2: # ensure that the teams are in alphabetical order
            temp = team1
            team1 = team2
            team2 = temp
            temp = odds1
            odds1 = odds2
            odds2 = temp
        self.name = team1 + " vs " + team2
        self.team1 = team1
        self.team2 = team2
        self.odds1 = odds1
        self.odds2 = odds2

    def checkForArbitrage(self, otherGame):
        if not (self.name == otherGame.name):
            return False
        if self.odds1 < 0 and self.odds2 > 0:
            if otherGame.odds2 <= 0:
                return False
            return self.odds2 > -(otherGame.odds1) or otherGame.odds2 > -(self.odds1)
        if self.odds1 > 0 and self.odds2 < 0:
            if otherGame.odds1 <= 0:
                return False
            return -self.odds2 < (otherGame.odds1) or -otherGame.odds2 < (self.odds1)
        return False

    def __str__(self):
        return self.name+": " + str(self.odds1) + " " + str(self.odds2)