from selenium.webdriver import Chrome
from Game import Game
from bs4 import BeautifulSoup
import random
import time

class ScraperBot(object):

    def __init__(self, name, url): #the url that corresponds to the sport nba/nfl/...
        self.teams = []
        self.odds = []
        self.games = {}
        self.name = name
        self.url = url
        self.driver = Chrome()
        self.driver.set_window_size(1280, 800)

    def getData(self):
        """
        This is the main method of the bot
        """
        self.clear()
        self.scrapePage()
        self.convertToDict()

    def clear(self):
        self.teams.clear()
        self.odds.clear()
        self.games.clear()

    def navigate(self):
        self.driver.get(self.url)

        ran = random.uniform(0.01,2)
        time.sleep(2)
        time.sleep(ran)

    #override this method always
    def scrapePage(self):
        """
        This method scrapes for teams and odds
        """
        soup = BeautifulSoup(self.driver.page_source, 'lxml')

    def convertToDict(self):
        """
        Converts the two arrays of teams and odds into a dictionary
        """
        numgames = len(self.teams)
        for i in range(numgames//2): # games should be even
            team1 = self.teams[2 * i].split()[-1]
            team2 = self.teams[2 * i + 1].split()[-1]
            odds1 = self.odds[2 * i]
            odds2 = self.odds[2 * i + 1]
            g = Game(team1, odds1, team2, odds2)
            self.games[g.name] = g