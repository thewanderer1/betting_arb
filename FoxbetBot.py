from bs4 import BeautifulSoup
from scraperBot import ScraperBot
import numpy as np
from Game import Game


class FoxbetBot(ScraperBot):

    # works for the following URLS as of 11/25/21
    # https://mi.foxbet.com/#/american_football/competitions/8707516 - NFL
    # https://mi.foxbet.com/#/basketball/competitions/8936422 - NBA
    # https://mi.foxbet.com/#/american_football/competitions/8211237 - NCAAF

    def __init__(self, name, url): #the url that corresponds to the sport nba/nfl/...
        super().__init__(name, url)

    def scrapePage(self):
        """
        tested for the following URLS as of 11/25/21
        https://mi.foxbet.com/#/american_football/competitions/8707516 - NFL
        https://mi.foxbet.com/#/basketball/competitions/8936422 - NBA
        https://mi.foxbet.com/#/american_football/competitions/8211237 - NCAAF
        """

        # load the html
        foxbet_soup = BeautifulSoup(self.driver.page_source, 'lxml')

        # get a list of all the games
        event = foxbet_soup.find('div', class_='market-content')
        games = event.find_all('section')

        # loop through the games and create a game object for each
        for game in games:
            l = len(self.odds)

            # get the team names
            teamlist = game.find_all('span', class_='teamName')
            # this list should have two elements
            team1 = teamlist[0].get_text().strip()
            # strip the team names to standardize them
            team1 = self.getTeamName(team1)
            team2 = teamlist[1].get_text().strip()
            team2 = self.getTeamName(team2)

            # for t in teamlist:
            #     self.teams.append(t.get_text().strip())

            # Get the odds
            # note the default value is zero in case the odds are missing
            odds = [0,0]

            # first get a list of all the odds (ML, spread, ...)
            # Get a pair of odds rows
            # there should be two elements in this list, one for each team
            oddslist = game.find_all('div', class_='afEvt__teamMarkets')

            for hos in oddslist:
                # get a list of the odds in this row
                alist = hos.find_all('a')

                # screen for moneyline odds using the class name
                for a in alist:
                    # the class name comes out as a split string
                    l2 = len(a['class'])
                    # the last 7 characters should be FTOT-ML
                    if not (l2 > 6 and a['class'][5][-7:] == "FTOT-ML"):
                        continue

                    # Get the numerical value of the odds
                    # if they are missing, put in zero
                    if len(a.find_all('em')) > 1:
                        odds[oddslist.index(hos)] = int(a.em.string.strip())
                    else:
                        odds[oddslist.index(hos)] = 0

            # create a Game object corresponding to this pair of rows
            game = Game(team1, odds[0], team2, odds[1])
            # if the same game is already in there (an earlier version), ignore the later game
            if game.name not in self.games:
                self.games[game.name] = game