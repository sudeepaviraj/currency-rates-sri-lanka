from scrape import save
import json


def output():
    with open("export.json","r") as file:
        print(json.loads(file.readline()))

def main(x):
    if(x=="2"):
        output()
    elif(x=="1"):
        scrape()

def scrape():
    try:
        print(" Please Wait... Scraping In Progress")
        save()
        print(" Scrape Successfull. Latest Data Saved To export.json")
    except Exception as e:
        print(" Scraping Failed.")
        print(e)
while(True):
    basic = str(input("Welcome To Currency Exchange Python Script\nPress Related Number To Continue\n 1.Scrape Latest Data\n 2.Print Scraped Data\n "))

    main(basic)