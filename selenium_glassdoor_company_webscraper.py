#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  9 17:12:25 2018

@author: Jonny Mills
"""

# -*- coding: utf-8 -*-

'''
Program summary: user inputs a list of companies. My program uses www.glassdoor.com to
to scrape information about each company, and returns column info about each company in an excel
file, sorted by overall highest company rating to lowest company rating.
'''

##Here is a link to view the code in action: https://www.youtube.com/watch?v=7HuJQllLijU

##########################
######IMPORT SECTION #####
##########################

import time 
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys #gives selenium access to keyboard
from selenium.common.exceptions import NoSuchElementException #error when selenium can't find certain element
import csv ##import exporting to csv stuff

#set working directory
import os
#path="/Users/default/Desktop/Python Spyder"
#os.chdir(path)


##########################
######FUNCTIONS ###########
##########################
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

#############################
###Get list of companies#####
#############################

reader = open("company_names.txt", "r")  ##
companies = reader.read().split('\n')
print("companies to scrape: ",companies)

##############################
######Launch Website #####
##############################
driver = webdriver.Chrome(executable_path = '/usr/local/bin/chromedriver' )
driver.get('https://www.glassdoor.com/Reviews/lexisnexis-reviews-SRCH_KE0,10.htm') #set up. Random company initially searched for because Glassdoor always opens a new tab when the first company is searched for, which we won't want
driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/div[2]/div[1]/div[2]/div[1]/a').click()
driver.get('https://www.glassdoor.com/Overview/Working-at-LexisNexis-EI_IE833178.11,21.htm')

links = [] #a list of all of links
company_not_found = [] #list of companies not found if Glassdoor does not contain company user inputted
all_company_data = [] #all of the 

for company in companies:
    #driver.find_element_by_xpath('//*[@id="TopNav"]/nav/div[2]/ul[2]/li[2]/a').click() #to go company tab
    
#############################
######Glassdoor Search##########
#############################

    ###################
    ###Company search##
    ####################
    
    company_search = driver.find_element_by_xpath('//*[@id="sc.keyword"]')
    company_search.clear()
    company_search.send_keys(company)
    company_search.send_keys(Keys.DOWN)
    company_search.send_keys(Keys.TAB) 
    
    #####################
    ####Location Search##
    #####################
    
    location_search = driver.find_element_by_xpath('//*[@id="sc.location"]')
    location_search.clear()
    location_search.send_keys(" ")   #user could put in any locaiton they wanted here
    driver.find_element_by_xpath('//*[@id="HeroSearchButton"]').click() #find the arrow and click
    
    if check_exists_by_xpath('//*[@id="MainCol"]/div[1]/div[2]/div[1]/div[2]/div[1]/a') == True: #if it doesn't go directly to the company page
        driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/div[2]/div[1]/div[2]/div[1]/a').click() #go to the company page
        #link = driver.current_url
        #links.append(link)                                  
    elif  check_exists_by_xpath('//*[@id="SearchSuggestions"]/p[1]') == True: #if the company isn't found
        company_not_found.append(company)
        continue
    #############################
    ######Extract text from Link##
    ############################## 
    link = driver.current_url
        #driver.get(link)
    attributes = [] #will contain information about each company
    
    try:
        attributes.append(driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/header/h2').text.split(" Overview")[0]) #company name
    except:
        attributes.append(" ")
    #print(attributes)
    try:
        attributes.append(driver.find_element_by_xpath('//*[@id="EmpStats"]/div/div[1]/div[1]').text) #overall rating
    except:
        attributes.append(" ")
    
    for xpathnum in range(1,8):
        try:
            attributes.append(driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[1]/div/div['+str(xpathnum)+']/span').text)
        except:
            attributes.append(" ")
            
    try:
        attributes.append(driver.find_element_by_xpath('//*[@id="EmpStats"]/div/div[2]/div[3]/div[1]/div[2]/div[1]').text) #CEO name
    except:
        try:
            attributes.append(driver.find_element_by_xpath('//*[@id="EmpStats"]/div/div[2]/div[3]/a/div/div[2]/div[1]').text) #Top CEO name 
        except:
            attributes.append(" ")
            
    try:
        attributes.append(driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[2]/div[2]/p').text) #mission statement
    except:
        try:
            attributes.append(driver.find_element_by_xpath('//*[@id="EmpBasicInfo"]/div[2]/div[1]').text) #longer mission statement
        except:
            attributes.append(" ")
    
    all_company_data.append(attributes)
    #driver.find_element_by_xpath=('//*[@id="EmpStats_Approve"]/svg/text')
    
print(all_company_data)


##############################
######sorting wizardry #######
##############################
all_company_data.sort(key=lambda x: x[1],reverse=True) #sort companies by overall rating


#replace k with 3 zeros
all_company_data

###############################################################################
###Output to CSV ##############################################################
###############################################################################

column_headers = ["Company name", "Overall Rating","Website", "Headquarters", "Size of company", "Year Founded", "Company type", "Industry", "Revenue", "CEO Name", "Company Mission/Description"]

### Write scraped data to CSV file

company_info_excel = open("output.csv",'w') 
writer = csv.writer(company_info_excel,delimiter= ',') #seperated intwo two steps to make it easier to close the CSV. See https://stackoverflow.com/questions/3347775/csv-writer-not-closing-file 

writer.writerow(column_headers)

for row in all_company_data: 
    try:
        writer.writerow(row)
    except:
        writer.writerow(' ')

[writer.writerow([row]) for row in company_not_found]

company_info_excel.close()


print ("done")


##########################
######Exit ###############
##########################
time.sleep(5) # sleep for 5 seconds so you can see the results
driver.quit() #exit the web program

