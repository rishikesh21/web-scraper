from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import os
import csv
import time
searchList=list();
#read the list and append it to a list
def readfile():
     with open('/Users/mac/Downloads/Companynames.csv') as csvfile:
         reader = csv.DictReader(csvfile)
         for row in reader:
             for year in range(2010,2018):
              searchList.append(row['company_name'] +"  Annual  Report-" + str(year) +" pdf")
#wait the driver until download is finished
def download_wait(path_to_downloads):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 20:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
    return seconds



if __name__ == '__main__':
    readfile()
    for i in range(len(searchList)):
           print(searchList[i])
           year=searchList[i].split("-")[1].replace(" pdf","")
           urls = []
           #launch url
           driver = webdriver.Chrome(executable_path='/Users/mac/Downloads/chromedriver')
           driver.get("https://google.com/search?query="+searchList[i])
           wait = WebDriverWait(driver, 9)
           all_urls = driver.find_elements_by_xpath("//a[contains(@href, '.pdf')]")
           urls.append([i.get_attribute("href") for i in all_urls])
           selected_urls=urls[0]
           new_url=[]
           new_url.append(("\',\'".join(s for s in selected_urls if year.lower() in s.lower())))
           #get download url
           wait = WebDriverWait(driver, 30)
           url=new_url[0].split("'")[0]
           print(url)
           driver.quit()
           #get the download done
           download_dir = "/Users/mac/Downloads/AnnualReport2010_2018/"
           profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],  # Disable Chrome's PDF Viewer
                 "download.default_directory": download_dir, "download.extensions_to_open": "applications/pdf"}
           options = webdriver.ChromeOptions()
           options.add_experimental_option("prefs", profile)
           download_driver = webdriver.Chrome(executable_path='/Users/mac/Downloads/chromedriver',chrome_options=options)
           download_driver.get(url)
           WebDriverWait(download_driver, 30)
           WebDriverWait(download_driver, download_wait("/Users/mac/Downloads/AnnualReport2010_2018/"))
           #shut down  the downloaddriver
           time.sleep(90)


           download_driver.quit()