from bs4 import BeautifulSoup
from scraperBot import ScraperBot
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from Game import Game

class GoldenNuggetBot(ScraperBot):

    def __init__(self, name, url): #the url that corresponds to the sport nba/nfl/...
        super().__init__(name, url)

    def scrapePage(self):
        """
        tested for the following URLS as of 11/25/21
        https://mi-casino.goldennuggetcasino.com/sports/sport/3/football/matches?preselectedFilters=13 - NFL
        https://mi-casino.goldennuggetcasino.com/sports/sport/3/football/matches?preselectedFilters=539 - NCAAF
        https://mi-casino.goldennuggetcasino.com/sports/sport/5/basketball/matches?preselectedFilters=all - All Basketball
        https://mi-casino.goldennuggetcasino.com/sports/sport/5/basketball/matches?preselectedFilters=543 - NBA
        """
        # try:
        #     element = self.driver.find_element_by_css_selector("a[class='content-loader__load-more-link']")
        #     ActionChains(self.driver).move_to_element(element).click().perform()
        # finally:
        #     a = 0
        # load the html
        soup = BeautifulSoup(self.driver.page_source, 'lxml')

        # get a list of all the games
        # note that some of the elements in this list do not correspond to games, but that shouldn't be a problem
        events = soup.find_all('li')

        # loop through all the games and make a Game for each one
        for event in events:
            # there is one hometeam and one away team per game
            hometeam = event.find('div', class_='event-card__body__name__home')
            awayteam = event.find('div', class_='event-card__body__name__away')

            # if this event is not a game, continue
            if not hometeam:
                continue

            team1 = hometeam.get_text().strip()
            # strip the team names to standardize them
            team1 = self.getTeamName(team1)
            team2 = awayteam.get_text().strip()
            team2 = self.getTeamName(team2)

            # get the moneyline odds as well
            # This is the column of odds so it has two odds
            moneyline = event.find('div', class_='market__body market__body--2-col market__body--HH')

            if not moneyline:
                continue

            # create something to store the odds
            # default value is a placeholder of zero
            odds = [0, 0]
            counter = 0
            # go through the column and get the individual odds
            for x in moneyline.find_all('span', class_='button--outcome__price'):
                odds[counter] =  int( x.get_text().strip() )
                counter+=1

            # create a Game object corresponding to this pair of rows
            game = Game(team1, odds[0], team2, odds[1])
            # put the game in the dictionary
            # if the same game is already in there (an earlier version), ignore the later game
            if game.name not in self.games:
                self.games[game.name] = game


    # overload the navigate method
    # an extra click is needed for this website
    def navigate(self):
        super(GoldenNuggetBot, self).navigate()

        # find the "See More button and click it
        try:
            element =  self.driver.find_element_by_xpath("//div[@class='main-content__content-canvas']//a[@class='content-loader__load-more-link']")
            ActionChains(self.driver).move_to_element(element).click().perform()
        except:
            print(" No see more button on " + self.name)

