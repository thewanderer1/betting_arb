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

class DraftkingsBot(ScraperBot):

    def __init__(self, url): #the url that corresponds to the sport nba/nfl/...
        super().__init__(url)

    def getData(self):
        foxbetsoup = BeautifulSoup(self.driver.page_source, 'lxml')
        events = foxbetsoup.find_all('tbody', class_='sportsbook-table__body')
        self.teams.clear()
        self.odds.clear()

        for e in events:
            barstool_teams_selector = e.find_all('div', class_='event-cell__name-text')
            barstool_odds_selector = e.find_all('span', class_='sportsbook-odds american no-margin default-color')
            tsl = 0
            osl = 0
            for t in barstool_teams_selector:
                self.teams.append(t.get_text().strip())
                tsl+=1

            for p in barstool_odds_selector:

                value = p.get_text().strip()
                osl += 1
                if value:
                    self.odds.append(value)
                else:
                    self.odds.append(0)

            for i in range(0,tsl - osl):
                self.odds.append(0) #placeholder for an odds value that isn't there yet(the value might be quickly changing or something else)

