# importing necessary libraries 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import re
import json
import warnings
warnings.filterwarnings("ignore")   


# define driver and get to the website for the data extraction 
driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
base_link = 'https://www.drugs.com/health-guide/' 
driver.get(base_link) 

# Scraping out all the terms present on the page, ignoring ones with brackets in them
names = driver.find_element_by_xpath('//*[@id="a-to-z"]/div[1]').text
nlist = []
for i in (''.join(names).split('\n')): # rohan\nsharma ==> ['rohan','sharma']
    if len(i) == 1:
        continue
    if '(' in i or ')' in i:
        continue
    else:
        # remove text within parentheses and convert to lowercase
        i = re.sub(r'(\([^)]*\))', '', i).strip().lower()
        # join words with dashes and add to nlist
        formatted_n = '-'.join(i.split())
        nlist.append(formatted_n)

# Once we have the list we can start our process
# creating list for the dictionaries we create for each query
data = []

for n in nlist: # looping over list of terms we obtained from the page
    dd = {}
    try:
        driver.get(base_link+n+'.html')
    except:  
        pass    
    try:
        symp = driver.find_element_by_xpath('//*[@id="content"]/div/ul')
        
        symp = symp.text.split('\n')
        # trtmnt = driver.find_element_xpath('//*[@id="content"]/div/p[15]/text()').text
        dd['symptom'] = symp
    except:  
        dd['symptom'] = ''   
    try:
        dd['information'] = driver.find_element_by_xpath('//*[@id="content"]/div/p[2]').text

    except:
        dd['information'] = ''    

    dd['disease'] = n
    try:
        dd['treatment_drugs'] = driver.find_element_by_xpath('//*[@id="content"]/div[2]/ul[4]').text.split('\n') # for getting information on treatements for the disease.
    except:  
        dd['treatment_drug'] = ''    
    # dd['treatment'] = trtmnt
    try:    
        dd['diagnosis'] = driver.find_element_by_xpath('//*[@id="content"]/div/p[12]').text
    except: 
        dd['diagnosis'] = ''
    try:
        dd['emergency_condition'] = driver.find_element_by_xpath('//*[@id="content"]/div[2]/ul[5]').text.split('\n')
    except:
        dd['emergency_condition'] = ''
    print(dd)    
    data.append(dd)
    
     
driver.quit()
# saving data in json format 
with open('diseases.json', 'w') as f:
    # dump the dictionary object to the file
    json.dump(data, f)    

df = pd.DataFrame(data)
df.to_csv('diseases_&_symptoms.csv')      
