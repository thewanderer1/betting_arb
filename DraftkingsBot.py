from bs4 import BeautifulSoup
from scraperBot import ScraperBot
from Game import Game


class DraftkingsBot(ScraperBot):

    def __init__(self, name, url): #the url that corresponds to the sport nba/nfl/...
        super().__init__(name, url)

    def scrapePage(self):
        """

                tested for the following URLS as of 11/26/21
                https://sportsbook.draftkings.com/leagues/football/88670561 - NFL
                https://sportsbook.draftkings.com/leagues/basketball/88670846 - NBA

        """
        # load the html using Beautiful Soup
        dksoup = BeautifulSoup(self.driver.page_source, 'lxml')

        # get a list of all the sportsbook tables that contain games
        tables = dksoup.find_all('tbody', class_='sportsbook-table__body')

        # get a list of all the rows (containing 1 set of team name and odds) in all the tables
        teamRowlist = []
        for t in tables:
            teamRowlist += t.find_all('tr')

        # this list should have an even number of rows
        numteams = len(teamRowlist)
        if numteams%2 != 0:
            print("Number of teams found on " + self.name + " is not even")
            return

        # loop through the list and create games from pairs of teams
        for i in range(numteams//2):
            # get the team names from pairs of rows
            team1 = teamRowlist[2 * i].find('div', class_='event-cell__name-text').get_text().strip()
            # strip the team names to standardize them
            team1 = self.getTeamName(team1)

            team2 = teamRowlist[2 * i + 1].find('div', class_='event-cell__name-text').get_text().strip()
            team2 = self.getTeamName(team2)

            # get the odds from pairs of rows
            odds1 = teamRowlist[2 * i].find('span', class_='sportsbook-odds american no-margin default-color')
            # check if the odds are there, otherwise set it as zero for a placeholder. This shouldn't set off any arbs
            # note odds will be negative if the odds are negative on the page
            if odds1:
                odds1 = int(odds1.get_text().strip())
            else:
                odds1 = 0

            odds2 = teamRowlist[2 * i + 1].find('span', class_='sportsbook-odds american no-margin default-color')
            if odds2:
                odds2 = int(odds2.get_text().strip())
            else:
                odds2 = 0

            # create a Game object corresponding to this pair of rows
            game = Game(team1, odds1, team2, odds2)
            # if the same game is already in there (an earlier version), ignore the later game
            if game.name not in self.games:
                self.games[game.name] = game