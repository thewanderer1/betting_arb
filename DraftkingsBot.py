from bs4 import BeautifulSoup
from scraperBot import ScraperBot

class DraftkingsBot(ScraperBot):

    def __init__(self, name, url): #the url that corresponds to the sport nba/nfl/...
        super().__init__(name, url)

    def scrapePage(self):
        dksoup = BeautifulSoup(self.driver.page_source, 'lxml')
        events = dksoup.find_all('tbody', class_='sportsbook-table__body')
        self.teams.clear()
        self.odds.clear()

        for e in events:
            dk_teams_selector = e.find_all('div', class_='event-cell__name-text')
            dk_odds_selector = e.find_all('span', class_='sportsbook-odds american no-margin default-color')
            tsl = 0
            osl = 0
            for t in dk_teams_selector:
                self.teams.append(t.get_text().strip())
                tsl+=1

            for p in dk_odds_selector:

                value = p.get_text().strip()
                osl += 1
                if value:
                    self.odds.append(int(value))
                else:
                    self.odds.append(0)

            for i in range(0,tsl - osl):
                self.odds.append(0) #placeholder for an odds value that isn't there yet(the value might be quickly changing or something else)

