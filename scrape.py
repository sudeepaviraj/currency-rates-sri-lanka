from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

options = Options()

# options.add_argument("--headless=new")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

def CentralBank():
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

def SampathBank():
    driver.get("https://www.sampath.lk/en/exchange-rates")

    table = driver.find_element(By.CLASS_NAME,"exch-rates")

    samp = BeautifulSoup(table.get_attribute("innerHTML"),"html.parser")

    rows = samp.find_all("tr")

    dataset = rows[-1].find_all("td")

    sampathreturn = {
        "source":"Sampath",
        "sell_rate":dataset[1].text,
        "buy_rate":dataset[3].text
    }
    print(sampathreturn)

def PeoplesBank():
    driver.get("https://www.peoplesbank.lk/exchange-rates/")

    peoples = driver.find_element(By.CLASS_NAME,"table")

    people = BeautifulSoup(peoples.get_attribute("innerHTML"),"html.parser")

    peoplerows = people.find_all("tr")

    print(peoplerows[2])

def NSBank():
    driver.get("https://www.nsb.lk/rates-tarriffs/exchange-rates/")

    nsbtable = driver.find_element(By.CLASS_NAME,"table")

    nsbsoup = BeautifulSoup(nsbtable.get_attribute("innerHTML"),"html.parser")

    nsbrows = nsbsoup.find_all("tr")

    nsbreturn = {
        "source":"NSB",
        "sell_rate":nsbrows[2].find_all("td")[-1].text,
        "buy_rate":nsbrows[2].find_all("td")[-2].text
    }

    print(nsbreturn)

    # print(nsbrows[2])

def GoogleFinance():
    driver.get("https://www.google.com/finance/quote/USD-LKR")
    rate = driver.find_element(By.CLASS_NAME,"kf1m0")
    finance = BeautifulSoup(rate.get_attribute("innerHTML"),"html.parser")
    finance.find("div")
    googlereturn = {
        "source":"Google",
        "sell_rate":finance.text,
        "buy_rate":finance.text
    }
    print(googlereturn)

SampathBank()

time.sleep(10)

