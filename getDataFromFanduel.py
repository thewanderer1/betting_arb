from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
#from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import random
import time
import twitter
import pudb


class ArbitrageBot(object):
    """docstring for ArbitrageBot"""
    def __init__(self):
        self.api = twitter.Api(consumer_key='YtALy1rMz8KaqP2XrqT9SSpe2',
                      consumer_secret='r4KzqjXO5XTX5O71AU5N6JtLuKQY2PGKPBNCGmJeHdos6TWcOc',
                      access_token_key='1358136718663245824-gGWy53o2cSWhpbkPtJ7UXQMyA0n7QN',
                      access_token_secret='QV7r5a7fQAMabCRyIJGKsnP8xKd6H6KcRSz3ty8l3pBaR')
        self.fanduel_teams = []
        self.fanduel_odds = []
        self.barstool_teams = []
        self.barstool_odds = []
        self.arbitrage_opportunities =[]

    def post_to_twitter(self,barstool_name,fanduel_name,barstool_odds,fanduel_odds):

        self.status = self.api.PostUpdate('bs:'+barstool_name+'/'+str(barstool_odds)+' fd:'+fanduel_name+'/'+str(fanduel_odds))


    def navigateToFanduel(self,driver):
        driver.get("https://sportsbook.fanduel.com")

        ran = random.uniform(0.01,2)
        time.sleep(ran)

        #driver.find_element_by_xpath("//a[@href='/sports/navigation/830.1']").click()
        driver.get("https://sportsbook.fanduel.com/sports/navigation/830.1/10107.3")

        ran = random.uniform(0.01,2)
        time.sleep(ran)

    def navigateToBarstool_upcoming(self,driver):
        driver.get("https://www.barstoolsportsbook.com/sports/basketball/nba")

        ran = random.uniform(0.01,2)
        time.sleep(ran)

    def navigateToBarstool_live(self,driver):
        driver.get("https://www.barstoolsportsbook.com/sports/basketball/nba?list=live")

        ran = random.uniform(0.01,2)
        time.sleep(ran)


    def getDataFromFanduel(self,driver):
        fanduel_soup = BeautifulSoup(driver.page_source, 'lxml')
        self.fanduel_teams.clear()
        self.fanduel_odds.clear()
        fanduel_teams_selector = fanduel_soup.find_all('span', class_='name')
        fanduel_odds_selector = fanduel_soup.find_all('div', class_='selectionprice')
        counter = 0
        for t in fanduel_teams_selector:
            self.fanduel_teams.append(t.get_text().strip())

        for p in fanduel_odds_selector:
            if(counter%6 == 2 or counter%6 == 3):
                s = p.get_text().strip()
                try:
                    self.fanduel_odds.append(int(s))
                except ValueError:
                    self.fanduel_odds.append(0) #placeholder for an odds value that isn't there yet(the value might be quickly changing or something else)

            counter = counter + 1

    def getDataFromBarstool(self,driver):
        barstool_soup = BeautifulSoup(driver.page_source, 'lxml')
        self.barstool_teams.clear()
        self.barstool_odds.clear()
        barstool_teams_selector = barstool_soup.find_all('p', class_='body1 participant upcoming')
        barstool_odds_selector = barstool_soup.find_all('label', class_='outcome-card label event-chip-wrapper')
        counter = 0
        for t in barstool_teams_selector:
            self.barstool_teams.append(t.get_text().strip())

        for p in barstool_odds_selector:
            if(counter%6 == 2 or counter%6 == 3):
                s = p["aria-label"]
                x = s.find("Odds:", 0, len(s))
                s1 = s[x:][6:]
                try:
                    self.barstool_odds.append(int(s1))
                except ValueError:
                    self.barstool_odds.append(0) #placeholder for an odds value that isn't there yet(the value might be quickly changing or something else)

            counter = counter + 1

#this is going to have to be redone - the empty cards in barstool go down a different HTML tree

    def getDataFromBarstool_live(self,driver):
        barstool_soup = BeautifulSoup(driver.page_source, 'lxml')
        events = barstool_soup.find_all('p', class_='container wrap event-row match-row')

        for e in events:
            
            
        barstool_odds_selector = barstool_soup.find_all('label', class_='outcome-card label event-chip-wrapper')
        counter = 0
        for t in barstool_teams_selector:
            self.barstool_teams.append(t.get_text().strip())

        for p in barstool_odds_selector:
            if(counter%6 == 2 or counter%6 == 3):
                s = p["aria-label"]
                x = s.find("Odds:", 0, len(s))
                s1 = s[x:][6:]
                try:
                    self.barstool_odds.append(int(s1))
                except ValueError:
                    self.barstool_odds.append(0) #placeholder for an odds value that isn't there yet(the value might be quickly changing or something else)

            counter = counter + 1


    def checkForArbitrage(self):
        for i in range(len(self.barstool_teams)//2): 
            for j in range(len(self.fanduel_teams)//2):
                if self.barstool_teams[2*i][len(self.barstool_teams[2*i]) - 4:] == self.fanduel_teams[2*j][len(self.fanduel_teams[2*j]) - 4:]: #check if the team names are the same
                    if(self.barstool_odds[2*i] > 0):
                        if(self.fanduel_odds[2*j+1] < 0 and -self.fanduel_odds[2*j+1] < self.barstool_odds[2*i]):
                            arbopp_name = self.barstool_teams[2*i][len(self.barstool_teams[2*i]) - 4:] + self.fanduel_teams[2*j+1][len(self.fanduel_teams[2*j+1]) - 4:] + str(self.barstool_odds[2*i])+str(self.fanduel_odds[2*j+1])
                            if arbopp_name not in self.arbitrage_opportunities:
                                self.arbitrage_opportunities.append(arbopp_name)
                                self.post_to_twitter(self.barstool_teams[2*i],self.fanduel_teams[2*j+1],self.barstool_odds[2*i],self.fanduel_odds[2*j+1])
                                print('Arbitrage found')


                    if(self.barstool_odds[2*i+1] > 0):
                        if(self.fanduel_odds[2*j] < 0 and -self.fanduel_odds[2*j] < self.barstool_odds[2*i+1]):
                            arbopp_name = self.barstool_teams[2*i+1][len(self.barstool_teams[2*i+1]) - 4:] + self.fanduel_teams[2*j][len(self.fanduel_teams[2*j]) - 4:] + str(self.barstool_odds[2*i+1])+str(self.fanduel_odds[2*j])
                            if arbopp_name not in self.arbitrage_opportunities:
                                self.arbitrage_opportunities.append(arbopp_name)
                                self.post_to_twitter(self.barstool_teams[2*i+1],self.fanduel_teams[2*j],self.barstool_odds[2*i+1],self.fanduel_odds[2*j])
                                print('Arbitrage found')

                    if(self.fanduel_odds[2*i] > 0):
                        if(self.barstool_odds[2*i+1] < 0 and -self.barstool_odds[2*i+1] < self.fanduel_odds[2*j]):
                            arbopp_name = self.barstool_teams[2*i+1][len(self.barstool_teams[2*i+1]) - 4:] + self.fanduel_teams[2*j][len(self.fanduel_teams[2*j]) - 4:] + str(self.barstool_odds[2*i+1])+str(self.fanduel_odds[2*j])
                            if arbopp_name not in self.arbitrage_opportunities:
                                self.arbitrage_opportunities.append(arbopp_name)
                                self.post_to_twitter(self.barstool_teams[2*i+1],self.fanduel_teams[2*j],self.barstool_odds[2*i+1],self.fanduel_odds[2*j])
                                print('Arbitrage found')

                    if(self.fanduel_odds[2*i+1] > 0):
                        if(self.barstool_odds[2*i] < 0 and -self.barstool_odds[2*i] < self.fanduel_odds[2*j+1]):
                            arbopp_name = self.barstool_teams[2*i][len(self.barstool_teams[2*i]) - 4:] + self.fanduel_teams[2*j+1][len(self.fanduel_teams[2*j+1]) - 4:] + str(self.barstool_odds[2*i])+str(self.fanduel_odds[2*j+1])
                            if arbopp_name not in self.arbitrage_opportunities:
                                self.arbitrage_opportunities.append(arbopp_name)
                                self.post_to_twitter(self.barstool_teams[2*i],self.fanduel_teams[2*j+1],self.barstool_odds[2*i],self.fanduel_odds[2*j+1])
                                print('Arbitrage found')


    def run(self):
        profile = webdriver.FirefoxProfile()

        PROXY_HOST = "12.12.12.123"
        PROXY_PORT = "1234"
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", PROXY_HOST)
        profile.set_preference("network.proxy.http_port", int(PROXY_PORT))
        profile.set_preference("dom.webdriver.enabled", False)
        profile.set_preference('useAutomationExtension', False)
        profile.update_preferences()
        desired = DesiredCapabilities.FIREFOX

        #ua = UserAgent()
        #userAgent = ua.random
        options = Options()
        #options.add_argument('-headless')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
        options.add_argument('--disable-blink-features=AutomationControlled')
        #firefoxOptions = webdriver.FirefoxOptions()
        #firefoxOptions.headless = True

        fanduel_driver = Chrome()
        barstool_driver_upcoming = Chrome()
        barstool_driver_live = Chrome()

        #try:
            #driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"})
        fanduel_driver.set_window_size(1280, 800)

        #barstool_driver.execute_script("Page.addScriptToEvaluateOnNewDocument", {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"})
        barstool_driver_upcoming.set_window_size(1280, 800)
        barstool_driver_live.set_window_size(1280, 800)

        self.navigateToFanduel(fanduel_driver)
        fanduelWindow = fanduel_driver.current_window_handle

      
        """body = driver.find_element_by_tag_name("body")
        body.send_keys(Keys.CONTROL + 't')

        for window_handle in driver.window_handles:
            if window_handle != fanduelWindow:
                driver.switch_to.window(window_handle)
                break"""

        self.navigateToBarstool_upcoming(barstool_driver_upcoming)

        self.navigateToBarstool_live(barstool_driver_live)

        time.sleep(5)
        #barstoolWindow=driver.current_window_handle



        while (True):
            time.sleep(.9)
            #switchToWindow(barstoolWindow)g
            self.getDataFromBarstool(barstool_driver_upcoming)
            self.getDataFromBarstool_live(barstool_driver_live)
            #switchToWindow(fanduelWindow)
            self.getDataFromFanduel(fanduel_driver)

            print(len(self.barstool_teams))
            print(len(self.barstool_odds))
            print(len(self.fanduel_teams))
            print(len(self.fanduel_odds))
            self.checkForArbitrage()

            print('hi')

            print("\nBarstool:")
            for p in self.barstool_teams:
                print(p)
            print("\nFanduel:")
            for p in self.fanduel_teams:
                print(p)


def main():
    a = ArbitrageBot()
    a.run()

if __name__ == '__main__':
    main()
