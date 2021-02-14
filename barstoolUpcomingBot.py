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

class BarstoolUpcomingBot(ScraperBot):

    def __init__(self, url): #the url that corresponds to the sport nba/nfl/...
        super().__init__(url)

    def getData(self):
        barstool_soup = BeautifulSoup(self.driver.page_source, 'lxml')
        self.teams.clear()
        self.odds.clear()
        barstool_teams_selector = barstool_soup.find_all('p', class_='body1 participant upcoming')
        barstool_odds_selector = barstool_soup.find_all('label', class_='outcome-card label event-chip-wrapper')
        counter = 0
        for t in barstool_teams_selector:
            self.teams.append(t.get_text().strip())

        for p in barstool_odds_selector:
            if(counter%6 == 2 or counter%6 == 3):
                s = p["aria-label"]
                x = s.find("Odds:", 0, len(s))
                s1 = s[x:][6:]
                try:
                    self.odds.append(int(s1))
                except ValueError:
                    self.odds.append(0) #placeholder for an odds value that isn't there yet(the value might be quickly changing or something else)

            counter = counter + 1