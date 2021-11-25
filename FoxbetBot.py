from bs4 import BeautifulSoup
from scraperBot import ScraperBot
import numpy as np

class FoxbetBot(ScraperBot):

    def __init__(self, url): #the url that corresponds to the sport nba/nfl/...
        super().__init__(url)

    def getData(self):
        """
        Note: This has been tested on NFL, NCAAF, MLB as of 9/18/21 and should work on NBA and anything with the 3 bet types
        """
        self.teams.clear()
        self.odds.clear()

        foxbet_soup = BeautifulSoup(self.driver.page_source, 'lxml')
        event = foxbet_soup.find('div', class_='market-content')
        games = event.find_all('section')


        for game in games:
            l = len(self.odds)
            teamlist = game.find_all('span', class_='teamName')
            for t in teamlist:
                self.teams.append(t.get_text().strip())

            oddslist = game.find_all('div', class_='afEvt__teamMarkets')
            for hos in oddslist: # there should be two elements in this list, one for each team
                alist = hos.find_all('a')
                counter = -1
                for a in alist: #
                    l2 = len(a['class'])
                    if l2 > 6:
                        l3 = len(a['class'][5])
                    if not (l2 > 6 and a['class'][5][(l3 - 7):] == "FTOT-ML"): # screen for moneyline odds
                        continue
                    if len(a.find_all('em')) > 1:
                        self.odds.append(int(a.em.string.strip())) # get the odds
                    else:
                        self.odds.append(0) # the value is not there, it is being updated. The zero acts as a placeholder

