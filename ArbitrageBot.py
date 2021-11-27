import time
import twitter
from datetime import datetime


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
                neg = -game2.odds1
                negteam = game2.team1
                negbook = name2
            if game2.odds2 > -(game1.odds1):
                pos = game2.odds2
                posteam = game2.team2
                posbook = name2
                neg = -game1.odds1
                negteam = game1.team1
                negbook = name1
        if game1.odds1 > 0 and game1.odds2 < 0:
            if game1.odds1 > -(game2.odds2):
                pos = game1.odds1
                posteam = game1.team1
                posbook = name1
                neg = -game2.odds2
                negteam = game2.team2
                negbook = name2
            if game2.odds1 > -(game1.odds2):
                pos = game2.odds1
                posteam = game2.team1
                posbook = name2
                neg = -game1.odds2
                negteam = game1.team2
                negbook = name1
        ratio = (pos + 100) * neg / ((neg + 100) * 100)


        post = "Arbitrage found \n" + name1 + ": " + str(game1) + "\n" + name2 + ": " + str(game2) + "\n\n" + "For every dollar bet on " + posbook + ": " + posteam + " bet " + str(ratio) + " dollars on " + negbook + ": " + negteam + "\n\n" + "The guaranteed profit per dollar is " + str(pos/100 - ratio)
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
                    # check that they aren't the same sportsbook so that we don't accidentally have crossover between ncaa teams who are the same
                    # check the first word in the book name
                    if gamelist[i].name.split()[0] == gamelist[j].name.split()[0]:
                        continue
                    if (gamelist[i].games[gameName].checkForArbitrage(gamelist[j].games[gameName])):
                        self.post_to_twitter(gamelist[i].name, gamelist[i].games[gameName], gamelist[j].name, gamelist[j].games[gameName])

    def run(self):
        for bot in self.scraperlist:
            bot.navigate()
        time.sleep(5)

        while (True):
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            print("Checking at time ", current_time)
            time.sleep(.9)
            for bot in self.scraperlist:
                bot.getData()
                # print(bot.name)
                # for game in bot.games:
                #     print(bot.games[game])
                # print(" ")
            self.checkForArbitrage()

