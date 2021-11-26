from bs4 import BeautifulSoup
from scraperBot import ScraperBot

class BarstoolUpcomingBot(ScraperBot):

    def __init__(self,name, url): #the url that corresponds to the sport nba/nfl/...
        super().__init__(name, url)

    def scrapePage(self):
        """

                        tested for the following URLS as of 11/26/21
                       - NFL
                        https://www.barstoolsportsbook.com/sports/basketball/nba - NBA

        """
        barstool_soup = BeautifulSoup(self.driver.page_source, 'lxml')
        events = barstool_soup.find_all('div', class_='container wrap event-row match-row')
        self.teams.clear()
        self.odds.clear()

        for e in events:
            barstool_teams_selector = e.find_all('p', class_='body1 participant upcoming')
            barstool_odds_selector = e.find_all('label', class_='outcome-card label event-chip-wrapper')
            tsl = 0
            osl = 0
            for t in barstool_teams_selector:
                self.teams.append(t.get_text().strip())
                tsl+=1

            for p in barstool_odds_selector:
                    s = p["aria-label"]
                    if(s.find("moneyline") >= 0):
                        osl+=1
                        x = s.find("Odds:", 0, len(s))
                        s1 = s[x:][6:]
                        try:
                            self.odds.append(int(s1))
                        except ValueError:
                            self.odds.append(0) #placeholder for an odds value that isn't there yet(the value might be quickly changing or something else)
            for i in range(0,tsl - osl):
                self.odds.append(0) #placeholder for an odds value that isn't there yet(the value might be quickly changing or something else)
