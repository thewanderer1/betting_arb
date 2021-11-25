
from bs4 import BeautifulSoup
from scraperBot import ScraperBot
from selenium.webdriver.common.by import By

class GoldenNuggetBot(ScraperBot):

    def __init__(self, url): #the url that corresponds to the sport nba/nfl/...
        super().__init__(url)

    def getData(self):
        """
        Note: This has been tested on NFL, NCAAF, MLB as of 9/18/21 and should work on NBA and anything with the 3 bet types
        """
        self.driver.find_element(By.CSS_SELECTOR, "[class='content-loader__load-more-link']").click()
        self.teams.clear()
        self.odds.clear()

        soup = BeautifulSoup(self.driver.page_source, 'lxml')
        hometeamslist = soup.find_all('div', class_='event-card__body__name__home')
        awayteamslist = soup.find_all('div', class_='event-card__body__name__away')
        moneylinelist = soup.find_all('div', class_='market__body market__body--2-col market__body--HH')
        for i in range(len(hometeamslist)):
            self.teams.append(hometeamslist[i].get_text().strip())
            self.teams.append(awayteamslist[i].get_text().strip())

        for m in moneylinelist:
            for x in m.find_all('span', class_='button--outcome__price'):
                self.odds.append( int( x.get_text().strip() ) )


