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
from scraperBot import ScraperBot

class FanduelLiveBot(ScraperBot):

    def __init__(self, url): #the url that corresponds to the sport nba/nfl/...
        super().__init__(url)

    def getData(self):
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        self.teams.clear()
        self.odds.clear()
        game_selector = soup.find_all('div', class_='r w hz h')
        counter = 0
        for g in game_selector:
            ts = g.find_all('span', class_='r w if ig ih ii ho hp hq hu ij h fv as ik bm')
            ps = g.find_all('div', class_='ip iq ao fc iz ja av')
            tsl = 0
            osl = 0
            for t in ts:
                tsl+=1
                self.teams.append(t.get_text().strip())
            for p in ps:
                    osl+=1
                    s = p.get_text().strip()
                    try:
                        self.odds.append(int(s))
                    except ValueError:
                        self.odds.append(0) #placeholder for an odds value that isn't there yet(the value might be quickly changing or something else)
           
            for i in range(0,tsl - osl):
                self.odds.append(0) #placeholder for an odds value that isn't there yet(the value might be quickly changing or something else)


