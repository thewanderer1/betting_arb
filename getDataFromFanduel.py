from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
options = Options()
options.add_argument('--headless')
firefoxOptions = webdriver.FirefoxOptions()
firefoxOptions.headless = True

with webdriver.Firefox(options=options) as driver:

    driver = Firefox()
    driver.get("https://sportsbook.fanduel.com/sports/navigation/830.1/10107.3")
    time.sleep(10)
    print(driver.page_source)
    #soup = BeautifulSoup(driver.page_source, 'lxml')
    #teams = []
    #teams_selector = soup.find_all('span', class_='name')
    #for t in teams_selector:
    #    teams.append(t.get_text().strip())

    #for t in teams:
     #   print(t)



