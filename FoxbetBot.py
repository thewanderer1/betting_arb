from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
#from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import random
import time
import twitter
import pudb
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
            #oddslist = game.find_all('em', class_='button__bet__odds selectionOdds-event')#gives all 6 possible odds if they exist


            for hos in oddslist: # there should be two elements in this list, one for each team
                alist = hos.find_all('a')
                counter = -1
                for a in alist: #
                    if a.
                    if len(od)==1:
                        self.odds.append(int(od[0].get_text().strip()))
                    else:
                        self.odds.append(np.nan)

