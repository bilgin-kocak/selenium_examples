# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 22:25:06 2020

@author: kocak
"""
import pandas as pd
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
pathForChromeDriver = "C:\\Users\\kocak\\Downloads\\chromedriver.exe"
path = os.getcwd() +"\\"
def writePaperInfo(driver, instructor_name, researchId, path):
    driver.get("https://app.webofknowledge.com/author/search?lang=en_US&SID=C5RAnJKHZGOk5ixJC2Q")
    # Wait 10 seconds for page to load
    timeout = 10
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, "//button[@class='wui-toggle__opt ng-scope']")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()
    button = driver.find_element_by_xpath("//button[@class='wui-toggle__opt ng-scope']").click()
    form = driver.find_element_by_name("orcid")
    form.send_keys(researchId)
    # driver.implicitly_wait(0.5)
    time.sleep(0.25)
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='wat-search__submit-button-orcid']/button"))).click()
    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()
    # find_button = driver.find_element_by_xpath("//div[@class='wat-search__submit-button-orcid']/button")
    # find_button.click()
    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_all_elements_located((By.ID, "pageCount.top")))
    except TimeoutException:
        print("Timed out waiting for page to load")
        driver.quit()
    el = driver.find_element_by_id("pageCount.top")
    max_page = int(el.text)
    paper_names = []
    authors = []
    journal_names = []
    meta_data = []
    citations = []
    for j in range(max_page):
        try:
            WebDriverWait(driver, timeout).until(EC.visibility_of_all_elements_located((By.XPATH, "//a[@class='borderless-button wat-author-record-publication-title-link ng-binding']")))
        except TimeoutException:
            print("Timed out waiting for page to load")
            driver.quit()
        elements = driver.find_elements_by_xpath("//a[@class='borderless-button wat-author-record-publication-title-link ng-binding']")
        paper_names_temp = [element.text for element in elements]
        paper_names += paper_names_temp 
        more_buttons = driver.find_elements_by_xpath("//a[@class='wat-author-record-publications-author wat-author-record-publications-author__more-less ng-binding']")
        for button in more_buttons:
            button.click()
        elements = driver.find_elements_by_xpath("//div[@class='wui-descriptor wat-search-results-publications-authors wat-author-record-publications-authors']")
        authors_temp = [element.text for element in elements]
        for i in range(len(authors_temp)):
            if authors_temp[i][-4:] == "Less":
                authors_temp[i] = authors_temp[i][:-6]
        authors += authors_temp 
        elements = driver.find_elements_by_xpath("//div[@class='wat-search-results-publications-source__item wat-search-results-publications-source ng-binding ng-scope']")
        journal_names_temp = [element.text for element in elements]
        journal_names += journal_names_temp
        
        elements = driver.find_elements_by_xpath("//div[@class='wui-descriptor-uppercase wat-search-results-publications-source-section wat-author-record-publications-source-section']")
        meta_data_temp = [element.text for element in elements]
        meta_data += meta_data_temp
        paper_info = meta_data[1::2]
        years = [int(info[-4:]) for info in paper_info]
        elements = driver.find_elements_by_xpath("//div[@class='wat-author-record-publication-section-metric-count']")
        citations_temp = [element.text for element in elements]
        citations += citations_temp 
        citation_numbers = [int(citation.split("\n")[1]) for citation in citations]
        if j == max_page-1:
            break
        next_button = driver.find_element_by_xpath("//a[@class='paginationNext']").click()
        
    instructor = {"Paper Name": paper_names, "Authors":authors, "Journal Names":journal_names,
                  "Paper Info": paper_info, "Year":years, "Times Cited":citation_numbers}
    df = pd.DataFrame.from_dict(instructor)
    df.to_excel(path + instructor_name + ".xlsx")


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

options = webdriver.ChromeOptions()
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")
# options.add_argument("--headless")
driver = webdriver.Chrome(pathForChromeDriver,options=options)
for instructor_name in hocalar:
    writePaperInfo(driver, instructor_name, hocalar[instructor_name], path)
driver.quit()
