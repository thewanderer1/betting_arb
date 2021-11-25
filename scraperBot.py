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

class ScraperBot(object):

    def __init__(self, url): #the url that corresponds to the sport nba/nfl/...
        self.teams = []
        self.odds = []
        self.url = url
        self.driver = Chrome()
        self.driver.set_window_size(1280, 800)
        

    def navigate(self):
        self.driver.get(self.url)

        ran = random.uniform(0.01,2)
        time.sleep(2)
        time.sleep(ran)

    #override always
    def getData(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        self.teams.clear()
        self.odds.clear()
        teams_selector = soup.find_all('span', class_='name')
        odds_selector = soup.find_all('div', class_='selectionprice')
        counter = 0
        for t in teams_selector:
            self.teams.append(t.get_text().strip())

        for p in odds_selector:
            if(counter%6 == 2 or counter%6 == 3):
                s = p.get_text().strip()
                try:
                    self.odds.append(int(s))
                except ValueError:
                    self.odds.append(0) #placeholder for an odds value that isn't there yet(the value might be quickly changing or something else)

            counter = counter + 1