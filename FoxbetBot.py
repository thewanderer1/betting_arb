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
        foxbet_soup = BeautifulSoup(self.driver.page_source, 'lxml')
        event = foxbet_soup.find('div', class_='market-content')
        

        html_teams = event.find_all('span', class_='teamName')
        html_odds_struct =  event.find_all('div', class_='afEvt__teamMarkets')

        self.teams.clear()
        self.odds.clear()

        for t in html_teams:
            self.teams.append(t.get_text().strip())

        for hos in html_odds_struct:
            od = hos.a.em.get_text().strip()

            if od == 'OTB':
                self.odds.append(np.nan)
            else:
                self.odds.append(int(od))
