# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 15:17:20 2020

@author: kocak
"""
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
pathForChromeDriver = "C:\\Users\\kocak\\Downloads\\chromedriver.exe"
path = os.getcwd() +"\\"

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
# options.add_argument("--headless")
driver = webdriver.Chrome(pathForChromeDriver,options=options)
driver.get("https://ce.metu.edu.tr/en/faculty-members")


elements = driver.find_elements_by_xpath("//div[@class='person']")
instructors = [element.text.split("\n")[1] for element in elements]

orcıd =[]
for hoca in instructors:
    
    driver.get("https://orcid.org/orcid-search/search?searchQuery="+hoca)
    timeout = 10
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//tr[@class='ng-star-inserted']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()
    element = driver.find_element_by_xpath("//tr[@class='ng-star-inserted']")
    orcıd.append(element.text)

hocalar = {"İrem Dikmen Toker":"AAC-9737-2019",
           "Aslı Akçamete Güngör":"G-3116-2018",
           # "Güzide Atasoy Özcan":"Y-2320-2019",
           "Onur Behzat Tokdemir":"O-4718-2016",
           "İsmail Özgür Yaman":"AAL-7451-2020",
           "Serdar Göktepe":"B-9753-2008",
           "Çağla Meral Akgül":"K-8590-2013",
           "Kemal Önder Çetin":"AAF-9773-2019",
           "Zeynep Gülerce":"AAC-1974-2020",
           "Nejan Huvaj Sarıhan":"A-3586-2013",
           "Cüneyt Baykal":"J-2834-2017",
           "Zafer Bozkuş":"P-8997-2019",
           # "Mete Köken":"R-6834-2019",
           "Zuhal Akyürek":"Q-4297-2016",
           "İsmail Yücel":"AAF-3210-2019",
           "M. Tuğrul Yılmaz":"W-4730-2017",
           "Eray Baran":"K-8943-2012",
           "Barış Binici":"J-3251-2015",
           "Erdem Canbay":"Y-2955-2019",
           "Afşin Sarıtaş":"A-9880-2013",
           "Kağan Tuncay":"B-2674-2008",
           "Ahmet Türer":"A-4478-2016",
           # "Burcu Burak Bakır":"B-4074-2012",
           "Ozan Cem Çelik":"Q-4611-2017",
           # "Burhan Aleessa Alam":"V-5198-2019",
           }
orcid1 = [oo.split(" ")[0] for oo in orcıd]
df = pd.DataFrame.from_dict(instructor_dict)
instructor_dict = {"Researcher":instructors,"ORCID":orcid1}
for i, row in df.iterrows():
    try:
        df.loc[i,"Web of Science ResearcherID"] = hocalar[row["Researcher"]]
    except:
        continue

df.to_excel(path +"aas.xlsx")
driver.quit()
