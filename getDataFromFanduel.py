import time
import twitter
from fanduelBot import FanduelBot
from barstoolUpcomingBot import BarstoolUpcomingBot
from barstoolLiveBot import BarstoolLiveBot
from fanduelLiveBot import FanduelLiveBot
from DraftkingsBot import DraftkingsBot
from FoxbetBot import FoxbetBot
from GoldenNuggetBot import GoldenNuggetBot


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
        post = "Arbitrage found \n" + name1 + ": " + str(game1) + "\n" + name2 + ": " + str(game2)
        self.status = self.api.PostUpdate(post)

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
                self.mastergamelist.remove(g)
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



    #fanduelnba = FanduelBot("https://sportsbook.fanduel.com/sports/navigation/830.1/10107.3")
    # barstoolUpcomingnba = BarstoolUpcomingBot("https://www.barstoolsportsbook.com/sports/baseball/mlb")
    # barstoolLivenba = BarstoolLiveBot("https://www.barstoolsportsbook.com/sports/baseball/mlb?ist=live")
    # fanduelLivenba = FanduelLiveBot("https://sportsbook.fanduel.com/navigation/mlb")
    # a = ArbitrageBot(fanduelLivenba,barstoolLivenba)
    # a.run()

    # fanduelLiveMLB = FanduelLiveBot("https://sportsbook.fanduel.com/navigation/mlb")
    # fanduelLiveMLB.navigate()
    # fanduelLiveMLB.getData()
    # print(fanduelLiveMLB.teams)
    # print(fanduelLiveMLB.odds)

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
