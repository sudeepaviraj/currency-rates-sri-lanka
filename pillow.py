import requests
from PIL import Image,ImageDraw,ImageFont
from bs4 import BeautifulSoup

def SampathBank():
    url = "https://www.sampath.lk/en/exchange-rates"
    req = requests.get(url)
    page = BeautifulSoup(req.content,"html.parser")
    table = page.find("table",{"class":"exch-rates"})
    print(table)

SampathBank()
