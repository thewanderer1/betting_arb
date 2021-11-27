from selenium.webdriver import Chrome
from Game import Game
from bs4 import BeautifulSoup
import random
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class ScraperBot(object):

    def __init__(self, name, url): #the url that corresponds to the sport nba/nfl/...
        # initialize all the variables
        self.teams = []
        self.odds = []
        self.games = {}
        self.name = name
        self.url = url

        # start Chrome
        self.driver = Chrome()

        # set a regular window size
        self.driver.set_window_size(1280, 800)

    def getData(self):
        """
        This is the main method of the bot
        """
        # clear all the existing team and odds data just in case
        self.clear()

        # scrape the webpage to gather data
        self.scrapePage()


    def clear(self):
        self.teams.clear()
        self.odds.clear()
        self.games.clear()

    def navigate(self):
        self.driver.get(self.url)

        # sleep to make the behavior random and avoid bot detection
        ran = random.uniform(0.01,2)
        time.sleep(2)
        time.sleep(ran)

        # scroll to bottom to load all html elements and games
        self.scrollToBottom()


    #override this method always
    def scrapePage(self):
        """
        This method scrapes for teams and odds
        """
        # always the first line
        soup = BeautifulSoup(self.driver.page_source, 'lxml')

    def scrollToBottom(self):
        # first, we need to load all of the NFL teams on this page
        scrollpos = 250

        total_height = self.driver.execute_script("return document.body.scrollHeight")

        while scrollpos < total_height:
            string_to_write = "window.scrollTo(0,"
            string_to_write += str(scrollpos)
            string_to_write += ")"
            self.driver.execute_script(string_to_write)
            time.sleep(.25)
            scrollpos += 250
            total_height = (self.driver).execute_script("return document.body.scrollHeight")

        string_to_write = "window.scrollTo(0, "
        string_to_write += str(total_height)
        string_to_write += ");"
        self.driver.execute_script(string_to_write)

    def getTeamName(self, teamString):
        """
        The purpose of this method is to strip the team names from the html down to a common name, the unique name of the team
        """
        # just get the last word of the team name, it should be the same across sportsbooks.
        return teamString.split()[-1]