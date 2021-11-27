
from bs4 import BeautifulSoup
from scraperBot import ScraperBot
from Game import Game

class BarstoolLiveBot(ScraperBot):

    def __init__(self, name, url): #the url that corresponds to the sport nba/nfl/...
        super().__init__(name, url)

    def scrapePage(self):

        """

                tested for the following URLS as of 11/26/21
                 - NFL
                https://www.barstoolsportsbook.com/sports/basketball/nba?list=live - NBA

        """
        # load the html
        barstool_soup = BeautifulSoup(self.driver.page_source, 'lxml')

        # get a list of all the games
        events = barstool_soup.find_all('div', class_='container wrap event-row match-row')

        # loop through the games and create a Game for each
        for e in events:
            # get a list of all the teams
            # this should have length 2
            teamlist = e.find_all('p', class_='body1 participant upcoming')

            team1 = teamlist[0].get_text().strip()
            # strip the team names to standardize them
            team1 = self.getTeamName(team1)
            team2 = teamlist[1].get_text().strip()
            team2 = self.getTeamName(team2)

            # create something to store the odds
            # default value is a placeholder of zero
            odds = [0, 0]

            # get a list of all the odds
            # should have two values unless odds are missing
            oddslist = e.find_all('label', class_='outcome-card label event-chip-wrapper')

            # keep a counter of which odds value we are storing (1 or 2)
            counter = 0
            for p in oddslist:
                s = p["aria-label"]
                if (s.find("moneyline") >= 0):
                    x = s.find("Odds:", 0, len(s))
                    s1 = s[x:][6:]
                    try:
                        odds[counter] = int(s1)
                    except ValueError:
                        odds[counter] = 0
                    counter += 1

            # create a Game object corresponding to this pair of rows
            game = Game(team1, odds[0], team2, odds[1])
            # put the game in the dictionary
            # if the same game is already in there (an earlier version), ignore the later game
            if game.name not in self.games:
                self.games[game.name] = game
