import time
import twitter
from fanduelBot import FanduelBot
from barstoolUpcomingBot import BarstoolUpcomingBot
from barstoolLiveBot import BarstoolLiveBot
from fanduelLiveBot import FanduelLiveBot
from DraftkingsBot import DraftkingsBot
from FoxbetBot import FoxbetBot
from WilliamHillBot import WilliamHillBot

class ArbitrageBot(object):
    """docstring for ArbitrageBot"""
    def __init__(self, scraper1, scraper2):
        self.api = twitter.Api(consumer_key='YtALy1rMz8KaqP2XrqT9SSpe2',
                      consumer_secret='r4KzqjXO5XTX5O71AU5N6JtLuKQY2PGKPBNCGmJeHdos6TWcOc',
                      access_token_key='1358136718663245824-gGWy53o2cSWhpbkPtJ7UXQMyA0n7QN',
                      access_token_secret='QV7r5a7fQAMabCRyIJGKsnP8xKd6H6KcRSz3ty8l3pBaR')
        self.scraper1 = scraper1
        self.scraper2 = scraper2
        self.arbitrage_opportunities =[]

    def post_to_twitter(self,name1,name2,odds1,odds2):

        self.status = self.api.PostUpdate('bs:'+name1+'/'+str(odds1)+' fd:'+name2+'/'+str(odds2))

    def checkForArbitrage(self):
        for i in range(len(self.scraper2.odds)//2): 
            for j in range(len(self.scraper1.odds)//2):
                if self.scraper2.teams[2*i][len(self.scraper2.teams[2*i]) - 4:] == self.scraper1.teams[2*j][len(self.scraper1.teams[2*j]) - 4:]: #check if the team names are the same
                    if(self.scraper2.odds[2*i] > 0):
                        if(self.scraper1.odds[2*j+1] < 0 and -self.scraper1.odds[2*j+1] < self.scraper2.odds[2*i]):
                            arbopp_name = self.scraper2.teams[2*i][len(self.scraper2.teams[2*i]) - 4:] + self.scraper1.teams[2*j+1][len(self.scraper1.teams[2*j+1]) - 4:] + str(self.scraper2.odds[2*i])+str(self.scraper1.odds[2*j+1])
                            if arbopp_name not in self.arbitrage_opportunities:
                                self.arbitrage_opportunities.append(arbopp_name)
                                self.post_to_twitter(self.scraper2.teams[2*i],self.scraper1.teams[2*j+1],self.scraper2.odds[2*i],self.scraper1.odds[2*j+1])
                                print('Arbitrage found')


                    if(self.scraper2.odds[2*i+1] > 0):
                        if(self.scraper1.odds[2*j] < 0 and -self.scraper1.odds[2*j] < self.scraper2.odds[2*i+1]):
                            arbopp_name = self.scraper2.teams[2*i+1][len(self.scraper2.teams[2*i+1]) - 4:] + self.scraper1.teams[2*j][len(self.scraper1.teams[2*j]) - 4:] + str(self.scraper2.odds[2*i+1])+str(self.scraper1.odds[2*j])
                            if arbopp_name not in self.arbitrage_opportunities:
                                self.arbitrage_opportunities.append(arbopp_name)
                                self.post_to_twitter(self.scraper2.teams[2*i+1],self.scraper1.teams[2*j],self.scraper2.odds[2*i+1],self.scraper1.odds[2*j])
                                print('Arbitrage found')

                    if(self.scraper1.odds[2*i] > 0):
                        if(self.scraper2.odds[2*i+1] < 0 and -self.scraper2.odds[2*i+1] < self.scraper1.odds[2*j]):
                            arbopp_name = self.scraper2.teams[2*i+1][len(self.scraper2.teams[2*i+1]) - 4:] + self.scraper1.teams[2*j][len(self.scraper1.teams[2*j]) - 4:] + str(self.scraper2.odds[2*i+1])+str(self.scraper1.odds[2*j])
                            if arbopp_name not in self.arbitrage_opportunities:
                                self.arbitrage_opportunities.append(arbopp_name)
                                self.post_to_twitter(self.scraper2.teams[2*i+1],self.scraper1.teams[2*j],self.scraper2.odds[2*i+1],self.scraper1.odds[2*j])
                                print('Arbitrage found')

                    if(self.scraper1.odds[2*i+1] > 0):
                        if(self.scraper2.odds[2*i] < 0 and -self.scraper2.odds[2*i] < self.scraper1.odds[2*j+1]):
                            arbopp_name = self.scraper2.teams[2*i][len(self.scraper2.teams[2*i]) - 4:] + self.scraper1.teams[2*j+1][len(self.scraper1.teams[2*j+1]) - 4:] + str(self.scraper2.odds[2*i])+str(self.scraper1.odds[2*j+1])
                            if arbopp_name not in self.arbitrage_opportunities:
                                self.arbitrage_opportunities.append(arbopp_name)
                                self.post_to_twitter(self.scraper2.teams[2*i],self.scraper1.teams[2*j+1],self.scraper2.odds[2*i],self.scraper1.odds[2*j+1])
                                print('Arbitrage found')


    def run(self):
        self.scraper1.navigate()
        self.scraper2.navigate()
        time.sleep(5)

        while (True):
            time.sleep(.9)
            self.scraper1.getData()
            self.scraper2.getData()

            self.checkForArbitrage()



def main():
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

#    dkb = DraftkingsBot("https://sportsbook.draftkings.com/leagues/football/88670775")
#
#    dkb.navigate()
#
#    dkb.getData()
#
#    print(dkb.teams)
#    print(dkb.odds)

    # fbb = FoxbetBot('https://mi.foxbet.com/#/baseball/competitions/8661882')

    # fbb.navigate()

    # fbb.getData()
    # print(fbb.teams)
    # print(fbb.odds)
    
    wh = WilliamHillBot("https://www.williamhill.com/us/mi/bet/football")

    wh.navigate()

    wh.getData()

    print(wh.teams)
    print(wh.odds)



if __name__ == '__main__':
    main()
