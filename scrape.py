from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

options = Options()

options.headless = False


driver = webdriver.Chrome("/media/sudeepa/Common/Python/chromedriver",options=options)
driver.get("https://www.cbsl.gov.lk/en/rates-and-indicators/exchange-rates/daily-buy-and-sell-exchange-rates")
# assert "Python" in driver.title

driver.switch_to.frame("iFrameResizer2")
elem = driver.find_element(By.ID, "rangeType_range")
elem.click()
select = Select(driver.find_element(By.ID, "rangeValue"))
select.select_by_index(1)
submit = driver.find_element(By.NAME, "submit_button")
submit.click()

tables = driver.find_elements(By.CLASS_NAME, "table-responsive")

for table in tables:
    soup = BeautifulSoup(table.get_attribute('innerHTML'), "html.parser")
    usd_table = soup.find_all("table")

rates = []

for usd in usd_table:
    rows = usd.find_all("td")
    rates.append(rows[0:3])

print(("{} - {} - {}".format(rates[-1][0].text,rates[-1][1].text,rates[-1][2].text)))

driver.get("https://www.sampath.lk/en/exchange-rates")

table = driver.find_element(By.CLASS_NAME,"exch-rates")

samp = BeautifulSoup(table.get_attribute("innerHTML"),"html.parser")

rows = samp.find_all("tr")

print(rows[-1])

driver.get("https://www.peoplesbank.lk/exchange-rates/")

peoples = driver.find_element(By.CLASS_NAME,"table")

people = BeautifulSoup(peoples.get_attribute("innerHTML"),"html.parser")

peoplerows = people.find_all("tr")

print(peoplerows[2])

driver.get("https://www.nsb.lk/rates-tarriffs/exchange-rates/")

nsbtable = driver.find_element(By.CLASS_NAME,"table")

nsbsoup = BeautifulSoup(nsbtable.get_attribute("innerHTML"),"html.parser")

nsbrows = nsbsoup.find_all("tr")

print(nsbrows[2])

time.sleep(10)

