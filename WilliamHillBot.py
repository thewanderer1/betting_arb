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

class WilliamHillBot(ScraperBot):

    def __init__(self, url): #the url that corresponds to the sport nba/nfl/...
        super().__init__(url)

    def getData(self):
        whsoup = BeautifulSoup(self.driver.page_source, 'lxml')
        events = whsoup.find_all('div', class_='eventList')
        self.teams.clear()
        self.odds.clear()

        for e in events:
            wh_teams_selector = e.find_all('div', class_='teamNameContainer')
            wh_odds_selector = e.find_all('div', class_='oddsView')
            tsl = 0
            osl = 0
            for t in wh_teams_selector:
                self.teams.append(t.span.get_text().strip())
                tsl+=1

            for p in wh_odds_selector:
                value = p.find('div',class_='odds truncateText')
                osl += 1
                if value is None:
                    self.odds.append(0)
                else:
                    self.odds.append(value.get_text().strip())


