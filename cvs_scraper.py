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

driver = Chrome()

driver.set_window_size(1280, 800)

while True:
	ran = random.uniform(0.01,2)
	time.sleep(ran)

	driver.get('https://www.cvs.com/immunizations/covid-19-vaccine')

	soup = BeautifulSoup(driver.page_source, 'lxml')

	vac_data = soup.find_all('div', class_='interstitial aem-GridColumn aem-GridColumn--default--12')

	for v in vac_data:

		state_id =v.div.div['id']

		state_id = state_id.strip()

		state = state_id[-3:]
		print(state)

	break


