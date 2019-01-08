from bs4 import BeautifulSoup as bs
import requests
import pprint
import re
from selenium import webdriver
import selenium.webdriver.support.ui as ui
import time
import math
import csv


data = open('Policy-capturing_ProQuest_edit.csv','w')
url = 'http://proxy.library.georgetown.edu/login?url=https://search.proquest.com/search/1414237?accountid=11091'

fields = ['index','title','link','author','journal','year','abstract','subjects']
writer = csv.DictWriter(data,fieldnames=fields, lineterminator='\n', restval='.')
writer.writeheader()

abstract_dict = {1:'', 2:'_0'}
[abstract_dict.update({i: '_'+str(i-2)}) for i in range(3,101)]

driver = webdriver.Chrome()
driver.get(url)
results_N = driver.find_element_by_xpath('//*[@id="pqResultsCount"]').text.replace(',','')
N = [s for s in results_N.split(' ') if s.isdigit()][0]
print(N,'results found')

for i in range(1,int(N)+1):
    scraped = False
    counter = 0
    while (not scraped) and counter < 2:
        try:
            print('i =', i)
            title_xpath = '//*[@id="result-header-' + str(i) + '"]'
            author_xpath = '//*[@id="mldcopy' + str(i) + '"]/span[1]'
            jorunal_xpath = '//*[@id="mldcopy' + str(i) + '"]/span[2]'
            preview_click_xpath = '//*[@id="resultPreviewTrigger_' + str(i) + '"]'
            driver.find_element_by_xpath(preview_click_xpath).click()
            time.sleep(1)
            idx = i - 100*math.floor((i-1)/100)
            abstract_xpath = '//*[@id="resultPreviewLayerZone' + abstract_dict[idx] + '"]/div/p[2]'
            subject_xpath = '//*[@id="resultPreviewLayerZone' + abstract_dict[idx] + '"]/div/div[2]/div[2]/div[2]'

            title = driver.find_element_by_xpath(title_xpath).text
            author = driver.find_element_by_xpath(author_xpath).text
            journal = driver.find_element_by_xpath(jorunal_xpath).text
            try:
                abstract = driver.find_element_by_xpath(abstract_xpath).text
            except:
                try:
                    time.sleep(5)
                    abstract = driver.find_element_by_xpath(abstract_xpath).text
                except:
                    abstract = ''
            try:
                subject_list = driver.find_element_by_xpath(subject_xpath).text.replace('\n', ' ')
            except:
                try:
                    time.sleep(5)
                    subject_list = driver.find_element_by_xpath(subject_xpath).text.replace('\n', ' ')
                except:
                    subject_list = ''
            soup = bs(driver.find_element_by_xpath(title_xpath).get_attribute('innerHTML'),'html5lib')
            link = soup.findAll('a')[0]['href']
            try:
                year = [int(s) for s in journal.replace('(', ' ').replace(')', ' ').replace('.','').replace(':','').split(' ') if s.isdigit() and int(s) >= 1900 and int(s) <= 2018][0]
            except:
                year = ''
            writer.writerow({'index': i, 'title': title, 'link': link, 'author': author, 'journal': journal, 'year': year, 'abstract': abstract, 'subjects': subject_list})
            scraped = True
        except:
            counter += 1
            time.sleep(2)

    if i % 100 == 0:
        try:
            driver.find_element_by_xpath('//*[@id="mainContentRight"]/nav/ul/li[last()]/a/span[2]').click()
        except:
            try:
                driver.find_element_by_xpath('//*[@id="mainContentRight"]/nav/ul/li[9]/a/span[2]').click()
            except:
                driver.find_element_by_xpath('//*[@id="mainContentRight"]/nav/ul/li[7]/a/span[2]').click()
        time.sleep(3)
