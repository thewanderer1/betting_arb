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

        #first, we need to load all of the NFL teams on this page
        scrollpos = 250

        total_height = self.driver.execute_script("return document.body.scrollHeight")

        while scrollpos < total_height:
            string_to_write = "window.scrollTo(0, "
            string_to_write += str(scrollpos)
            string_to_write += ");"
            self.driver.execute_script(string_to_write)
            time.sleep(.25)
            scrollpos += 250
            total_height = self.driver.execute_script("return document.body.scrollHeight")

        string_to_write = "window.scrollTo(0, "
        string_to_write += str(total_height)
        string_to_write += ");"
        self.driver.execute_script(string_to_write)



        whsoup = BeautifulSoup(self.driver.page_source, 'lxml')
        nfl_teams_html = whsoup.find('div',class_='Expander has--toggle competitionExpander') #there are two of these, one for NFL and one for NCAA - NFL is always first
        events = nfl_teams_html.find_all('div', class_='eventList')
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


