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

fanduel_teams = []
fanduel_odds = []
barstool_teams = []
barstool_odds = []

def navigateToFanduel(driver):
    driver.get("https://sportsbook.fanduel.com")

    ran = random.uniform(0.01,2)
    time.sleep(ran)

    original_window = driver.current_window_handle

    driver.find_element_by_xpath("//a[@href='/sports/navigation/830.1']").click()
    #driver.get("https://sportsbook.fanduel.com/sports/navigation/830.1/10107.3")

    ran = random.uniform(0.01,2)
    time.sleep(ran)

def navigateToBarstool(driver):
    driver.get("https://www.barstoolsportsbook.com/sports/basketball/nba")

    ran = random.uniform(0.01,2)
    time.sleep(ran)

def getDataFromFanduel(driver):
    fanduel_soup = BeautifulSoup(driver.page_source, 'lxml')
    fanduel_teams.clear()
    fanduel_odds.clear()
    fanduel_teams_selector = fanduel_soup.find_all('span', class_='name')
    fanduel_odds_selector = fanduel_soup.find_all('div', class_='selectionprice')
    counter = 0
    for t in fanduel_teams_selector:
        fanduel_teams.append(t.get_text().strip())

    for p in fanduel_odds_selector:
        if(counter%6 == 2 or counter%6 == 3):
            s = p.get_text().strip()
            try:
                fanduel_odds.append(int(s))
            finally:
                fanduel_odds.append(0) #placeholder for an odds value that isn't there yet(the value might be quickly changing or something else)

        counter = counter + 1

def getDataFromBarstool(driver):
    barstool_soup = BeautifulSoup(driver.page_source, 'lxml')
    barstool_teams.clear()
    barstool_odds.clear()
    barstool_teams_selector = barstool_soup.find_all('p', class_='body1 participant upcoming')
    barstool_odds_selector = barstool_soup.find_all('label', class_='outcome-card label event-chip-wrapper')
    counter = 0
    for t in barstool_teams_selector:
        barstool_teams.append(t.get_text().strip())

    for p in barstool_odds_selector:
        if(counter%6 == 2 or counter%6 == 3):
            s = p["aria-label"]
            x = s.find("Odds:", 0, len(s))
            s1 = s[x:][6:]
            try:
                barstool_odds.append(int(s1))
            finally:
                barstool_odds.append(0) #placeholder for an odds value that isn't there yet(the value might be quickly changing or something else)

        counter = counter + 1

def switchToWindow(windowHandle):
    driver.switch_to().window(windowHandle)

def checkForArbitrage():
    for i in range(len(barstool_teams)//2): 
        for j in range(len(fanduel_teams)//2):
            if barstool_teams[2*i][len(barstool_teams[2*i]) - 4:] == fanduel_teams[2*j][len(fanduel_teams[2*j]) - 4:]: #check if the team names are the same
                if(barstool_odds[2*i] > 0):
                    if(fanduel_odds[2*j] < 0 and -fanduel_odds[2*j] < barstool_odds[2*i]):
                        print("Arbitrage found")
                    if(fanduel_odds[2*j+1] < 0 and -fanduel_odds[2*j+1] < barstool_odds[2*i]):
                        print("Arbitrage found")

                if(barstool_odds[2*i+1] > 0):
                    if(fanduel_odds[2*j] < 0 and -fanduel_odds[2*j] < barstool_odds[2*i+1]):
                        print("Arbitrage found")
                    if(fanduel_odds[2*j+1] < 0 and -fanduel_odds[2*j+1] < barstool_odds[2*i+1]):
                        print("Arbitrage found")

                if(fanduel_odds[2*i] > 0):
                    if(barstool_odds[2*i] < 0 and -barstool_odds[2*i] < fanduel_odds[2*j]):
                        print("Arbitrage found")
                    if(barstool_odds[2*i+1] < 0 and -barstool_odds[2*i+1] < fanduel_odds[2*j]):
                        print("Arbitrage found")

                if(barstool_odds[2*i+1] > 0):
                    if(barstool_odds[2*i] < 0 and -barstool_odds[2*i] < fanduel_odds[2*j+1]):
                        print("Arbitrage found")
                    if(barstool_odds[2*i+1] < 0 and -barstool_odds[2*i+1] < fanduel_odds[2*j+1]):
                        print("Arbitrage found")


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
#firefoxOptions = webdriver.FirefoxOptions()
#firefoxOptions.headless = True

driver = Chrome()
driver2 = Chrome()



try:
    #driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"})
    driver.set_window_size(1280, 800)

    #driver2.execute_script("Page.addScriptToEvaluateOnNewDocument", {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"})
    driver2.set_window_size(1280, 800)
    
    navigateToFanduel(driver)
    fanduelWindow= driver.current_window_handle

  
    """body = driver.find_element_by_tag_name("body")
    body.send_keys(Keys.CONTROL + 't')

    for window_handle in driver.window_handles:
        if window_handle != fanduelWindow:
            driver.switch_to.window(window_handle)
            break"""

    navigateToBarstool(driver2)
    time.sleep(5)
    #barstoolWindow=driver.current_window_handle

    while (True):
        #switchToWindow(barstoolWindow)
        getDataFromBarstool(driver2)
        #switchToWindow(fanduelWindow)
        getDataFromFanduel(driver)
        checkForArbitrage()
        print("\nBarstool:")
        for p in barstool_teams:
            print(p)
        print("\nFanduel:")
        for p in fanduel_teams:
            print(p)

    


    




finally:
    driver.quit()
    driver2.quit()



