from bs4 import BeautifulSoup
from scraperBot import ScraperBot
from Game import Game

class WilliamHillBot(ScraperBot):

    def __init__(self, name, url): #the url that corresponds to the sport nba/nfl/...
        super().__init__(name, url)

    def scrapePage(self):
        """
        Tested for the following URLs 11/26/21
        https://www.williamhill.com/us/mi/bet/basketball - NBA and NCAAB, only gets the first section which is NBA
        """

        # Load the html
        whsoup = BeautifulSoup(self.driver.page_source, 'lxml')

        # get the all the sets of games on the page
        leagues = whsoup.find_all('div',class_='Expander has--toggle competitionExpander') #there are two of these, one for NFL and one for NCAA - NFL is always first
        for l in leagues:
            # get a list of all the games in the each set
            events = l.find_all('div', class_='EventCard')

            # loop through all the games and make a Game for each
            for e in events:
                # Get the list of teams
                # there should be 2
                teamlist = e.find_all('div', class_='teamNameContainer')

                # double check that there are two teams
                if (len(teamlist) != 2):
                    continue

                team1 = teamlist[0].span.get_text().strip()
                # strip the team names to standardize them
                team1 = self.getTeamName(team1)
                team2 = teamlist[1].get_text().strip()
                team2 = self.getTeamName(team2)

                # get a list of all the odds
                # should have 6 values unless odds are missing
                oddslist = e.find_all('div', class_='odds truncateText')

                # create something to store the odds
                # default value is a placeholder of zero
                odds = [0, 0]

                if len(oddslist) >= 6:
                    counter = 0
                    for p in oddslist:
                        sb = p.find_previous_siblings()
                        if not sb:
                            try:
                                odds[counter] = int(p.get_text().strip())
                            except:
                                odds[counter]=0
                            counter +=1

                # create a Game object corresponding to this pair of rows
                game = Game(team1, odds[0], team2, odds[1])
                # put the game in the dictionary
                # if the same game is already in there (an earlier version), ignore the later game
                if game.name not in self.games:
                    self.games[game.name] = game

