from bs4 import BeautifulSoup
from scraperBot import ScraperBot

class WilliamHillBot(ScraperBot):

    def __init__(self, name, url): #the url that corresponds to the sport nba/nfl/...
        super().__init__(name, url)

    def scrapePage(self):
        """
        Tested for the following URLs 11/26/21
        https://www.williamhill.com/us/mi/bet/basketball - NBA and NCAAB, only gets the first section which is NBA
        """

        whsoup = BeautifulSoup(self.driver.page_source, 'lxml')
        nfl_teams_html = whsoup.find('div',class_='Expander has--toggle competitionExpander') #there are two of these, one for NFL and one for NCAA - NFL is always first
        events = nfl_teams_html.find_all('div', class_='EventCard')
        self.teams.clear()
        self.odds.clear()

        for e in events:
            wh_teams_selector = e.find_all('div', class_='teamNameContainer')
            wh_odds_selector = e.find_all('div', class_='odds truncateText')
            tsl = 0
            osl = 0
            for t in wh_teams_selector:
                self.teams.append(t.span.get_text().strip())
                tsl+=1
            if len(wh_odds_selector) < 6:
                self.odds.append(0)
                self.odds.append(0)
            else:
                for p in wh_odds_selector:
                    sb = p.find_previous_siblings()
                    if not sb:
                        osl += 1
                        self.odds.append(int(p.get_text().strip()))


