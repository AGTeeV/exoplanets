from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
from selenium.webdriver.common.by import By
import requests
import pandas as pd

starturl="https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser=webdriver.Chrome("chromedriver.exe")
browser.get(starturl)
time.sleep(10)
headers=["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date","hyperlink","planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]    
planetdata=[]    

def scrape():
    
    for i in range(1,204):
        while True:
            time.sleep(2)
            soup= BeautifulSoup(browser.page_source,"html.parser")
            currentpage=int(soup.find_all("input",attrs={"class",'page_num'})[0].get('value'))
            if currentpage<i:
                browser.find_element(By.XPATH,value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
            elif currentpage>i:
                browser.find_element(By.XPATH,value='//*[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
            else:
                break
        for ul in soup.find_all("ul",attrs={"class","exoplanet"}):
            litags=ul.find_all("li")
            templist=[]
            for index,li in enumerate(litags):
                if index==0:
                    templist.append(li.find_all('a')[0].contents[0])
                else:
                    try:
                        templist.append(li.contents[0])
                    except:
                        templist.append("")
            hyperlink=litags[0]
            templist.append("https://exoplanets.nasa.gov"+ hyperlink.find_all("a", href=True)[0]["href"])
            planetdata.append(templist)
        browser.find_element(By.XPATH,value='//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        print(f'page {i} completed')
scrape()

newplanetdata =[]
def scrapemoredata(x):
    try:
        page=requests.get(x)
        soup=BeautifulSoup(page.content,'html.parser')
        templist=[]
        for tr in soup.find_all('tr',attrs={'class':'fact_row'}):
            tdtags=tr.find_all('td')
            for td in tdtags:
                try:
                    templist.append(td.find_all('div',attrs={'class':'value'})[0].contents[0])
                except:
                    templist.append('')
        newplanetdata.append(templist)
    except:
        time.sleep(1)
        scrapemoredata(x)
for i,data in enumerate(planetdata):
    scrapemoredata(data[5])
    print(f"scraping at hyperlink {i+1} is completed")

finalplanetdata=[]
for i,data in enumerate(planetdata):
    newdata=newplanetdata[i]
    newdata=[e.replace("\n",'') for e in newdata]
    newdata=newdata[:7]
    finalplanetdata.append(data+newdata)
with open("127.csv","w") as x:
    writer=csv.writer(x)
    writer.writerow(headers)
    writer.writerows(planetdata)