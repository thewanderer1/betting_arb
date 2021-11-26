from bs4 import BeautifulSoup
from scraperBot import ScraperBot
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

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
        time.sleep(2)
        self.teams.clear()
        self.odds.clear()

        # delete list of promos in right panel to avoid any extra data or games or anything
        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        rightpanel = soup.find('div', class_='right-panels-group my-bets--floating')
        rightpanel.decompose()

        events = soup.find_all('li')
        for event in events:
            hometeamslist = event.find_all('div', class_='event-card__body__name__home')
            awayteamslist = event.find_all('div', class_='event-card__body__name__away')
            moneylinelist = event.find_all('div', class_='market__body market__body--2-col market__body--HH')
            for i in range(len(hometeamslist)):
                self.teams.append(hometeamslist[i].get_text().strip())
                self.teams.append(awayteamslist[i].get_text().strip())

            l1 = len(self.odds)
            for m in moneylinelist:
                for x in m.find_all('span', class_='button--outcome__price'):
                    self.odds.append( int( x.get_text().strip() ) )

            l2 = len(self.odds)
            for i in range(l1 + 2 * len(hometeamslist) - l2): #ensure that there are placeholders if the odds are missing
                self.odds.append(0)

    def navigate(self):
        super(GoldenNuggetBot, self).navigate()
        element = self.driver.find_element_by_css_selector("a[class='content-loader__load-more-link']")
        ActionChains(self.driver).move_to_element(element).click().perform()

