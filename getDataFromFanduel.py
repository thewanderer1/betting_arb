import time
import twitter
from fanduelBot import FanduelBot
from barstoolUpcomingBot import BarstoolUpcomingBot
from barstoolLiveBot import BarstoolLiveBot
from fanduelLiveBot import FanduelLiveBot
from DraftkingsBot import DraftkingsBot
from FoxbetBot import FoxbetBot
from GoldenNuggetBot import GoldenNuggetBot
from WilliamHillBot import WilliamHillBot

class ArbitrageBot(object):
    """docstring for ArbitrageBot"""
    def __init__(self, scraperlist):
        self.api = twitter.Api(consumer_key='YtALy1rMz8KaqP2XrqT9SSpe2',
                      consumer_secret='r4KzqjXO5XTX5O71AU5N6JtLuKQY2PGKPBNCGmJeHdos6TWcOc',
                      access_token_key='1358136718663245824-gGWy53o2cSWhpbkPtJ7UXQMyA0n7QN',
                      access_token_secret='QV7r5a7fQAMabCRyIJGKsnP8xKd6H6KcRSz3ty8l3pBaR')
        self.scraperlist = scraperlist
        self.mastergamelist = []
        self.arbitrage_opportunities =[]

    def calculateBetRatio(self, game1, game2):
        """
        calculate the betting ratio to maximize guaranteed profit
        """
        pos = 0
        neg = 0
        if game1.odds1 < 0 and game1.odds2 > 0:
            if game1.odds2 > -(game2.odds1):
                pos = game1.odds2
                neg = game2.odds1
            if game2.odds2 > -(game1.odds1):
                pos = game2.odds2
                neg = game1.odds1
        if game1.odds1 > 0 and game1.odds2 < 0:
            if game1.odds1 > -(game2.odds2):
                pos = game1.odds1
                neg = game2.odds2
            if game2.odds1 > -(game1.odds2):
                pos = game2.odds1
                neg = game1.odds2
        ratio = (pos + 100) * neg / ((neg + 100) * 100)
        return ratio

    def post_to_twitter(self,name1, game1, name2, game2):

        # First calculate the optimal betting ratio and which book/teams to bet on
        pos = 0
        posteam = ""
        posbook = ""
        neg = 0
        negteam = ""
        negbook = ""
        if game1.odds1 < 0 and game1.odds2 > 0:
            if game1.odds2 > -(game2.odds1):
                pos = game1.odds2
                posteam = game1.team2
                posbook = name1
                neg = game2.odds1
                negteam = game2.team1
                negbook = name2
            if game2.odds2 > -(game1.odds1):
                pos = game2.odds2
                posteam = game2.team2
                posbook = name2
                neg = game1.odds1
                negteam = game1.team1
                negbook = name1
        if game1.odds1 > 0 and game1.odds2 < 0:
            if game1.odds1 > -(game2.odds2):
                pos = game1.odds1
                posteam = game1.team1
                posbook = name1
                neg = game2.odds2
                negteam = game2.team2
                negbook = name2
            if game2.odds1 > -(game1.odds2):
                pos = game2.odds2
                posteam = game2.team2
                posbook = name2
                neg = game1.odds1
                negteam = game1.team1
                negbook = name1
        ratio = (pos + 100) * neg / ((neg + 100) * 100)


        post = "Arbitrage found \n" + name1 + ": " + str(game1) + "\n" + name2 + ": " + str(game2) + "\n" + "For every dollar bet on " + posbook + ": " + posteam + " bet " + str(ratio) + " dollars on " + negbook + ": " + negteam + "\n" + "The guaranteed profit per dollar is " + str(a/100 - ratio)
        try:
            self.status = self.api.PostUpdate(post)
        finally:
            return

    def checkForArbitrage(self):
        for bot in self.scraperlist:
            for gameName in bot.games:
                if gameName not in self.mastergamelist:
                    self.mastergamelist.append(gameName)

        for gameName in self.mastergamelist:
            gamelist = []
            for bot in self.scraperlist:
                if gameName in bot.games:
                    gamelist.append(bot)
            if len(gamelist) == 0:
                self.mastergamelist.remove(gameName)
                continue
            l = len(gamelist)
            for i in range(l):
                for j in range(i + 1, l):
                    if (gamelist[i].games[gameName].checkForArbitrage(gamelist[j].games[gameName])):
                        self.post_to_twitter(gamelist[i].name, gamelist[i].games[gameName], gamelist[j].name, gamelist[j].games[gameName])

    def run(self):
        for bot in self.scraperlist:
            bot.navigate()
        time.sleep(5)

        while (True):
            print("checking")
            time.sleep(.9)
            for bot in self.scraperlist:
                bot.getData()
            self.checkForArbitrage()



def main():

    NFLbots = []
    NFLbots.append(FoxbetBot("Foxbet NFL", 'https://mi.foxbet.com/#/american_football/competitions/8707516'))
    NFLbots.append(BarstoolUpcomingBot("Barstool Upcoming NFL", 'https://www.barstoolsportsbook.com/sports/american_football/nfl'))
    NFLbots.append(BarstoolLiveBot("Barstool Live NFL", 'https://www.barstoolsportsbook.com/sports/american_football/nfl?list=live'))
    NFLbots.append(GoldenNuggetBot("Golden Nugget NFL", 'https://mi-casino.goldennuggetcasino.com/sports/sport/3/football/matches?preselectedFilters=13'))
    NFLbots.append(DraftkingsBot("DraftKings NFL", 'https://sportsbook.draftkings.com/leagues/football/88670561'))

    a = ArbitrageBot(NFLbots)
    a.run()

    """fbb = FoxbetBot('https://mi.foxbet.com/#/american_football/competitions/8211237')
    fbb.navigate()
    fbb.getData()
    print(fbb.teams)
    print(fbb.odds)""" #

    """fbb = FanduelBot("https://sportsbook.fanduel.com/sports/navigation/830.1/10107.3")
    fbb.navigate()
    fbb.getData()
    print(fbb.teams)
    print(fbb.odds)""" #doesn't work

    """bub = BarstoolUpcomingBot('https://www.barstoolsportsbook.com/sports/basketball/nba')
    bub.navigate()
    bub.getData()
    print(bub.teams)
    print(bub.odds)""" # works

    """blb = BarstoolLiveBot('https://www.barstoolsportsbook.com/sports/american_football/ncaaf?list=live')
    blb.navigate()
    blb.getData()
    print(blb.teams)
    print(blb.odds)""" # works

    """gnb = GoldenNuggetBot('https://mi-casino.goldennuggetcasino.com/sports/sport/5/basketball/matches?preselectedFilters=all')
    gnb.navigate()
    gnb.getData()
    print(gnb.teams)
    print(gnb.odds)""" # partially works

    """dkb = DraftkingsBot('https://sportsbook.draftkings.com/leagues/football/88670561')
    dkb.navigate()
    dkb.getData()
    print(dkb.teams)
    print(dkb.odds)"""



if __name__ == '__main__':
    main()
