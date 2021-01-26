from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import random
import time



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

ua = UserAgent()
userAgent = ua.random
options = Options()
#options.add_argument('-headless')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
#firefoxOptions = webdriver.FirefoxOptions()
#firefoxOptions.headless = True

driver = webdriver.Firefox(firefox_profile=profile, desired_capabilities=desired, options=options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.set_window_size(1280, 800)
driver.get("https://sportsbook.fanduel.com")

ran = random.uniform(0.01,2)
time.sleep(ran)

driver.find_element_by_xpath("//a[@href='/sports/navigation/830.1']").click()
#driver.get("https://sportsbook.fanduel.com/sports/navigation/830.1/10107.3")

ran = random.uniform(0.01,2)
time.sleep(ran)

soup = BeautifulSoup(driver.page_source, 'lxml')
teams = []
odds = []
teams_selector = soup.find_all('span', class_='name')
odds_selector = soup.find_all('div', class_='selectionprice')
counter = 0
for t in teams_selector:
    teams.append(t.get_text().strip())

for p in odds_selector:
    if(counter%6 == 2 or counter%6 == 3):
        odds.append(int(p.get_text().strip()))

    counter = counter + 1

for t in teams:
    print(t)

for p in odds:
    print(p)
    
driver.quit()



