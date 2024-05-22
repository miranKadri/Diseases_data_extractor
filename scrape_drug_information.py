# importing necessary libraries 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import re
import json
import warnings 
warnings.filterwarnings("ignore")   

# define driver and get to the website for the data extraction   
driver = webdriver.Chrome(executable_path=r"chromedriver.exe")
base_link = 'https://www.drugs.com/'
driver.get(base_link + 'drug_information.html')  

# Scraping out all the terms present on the page, ignoring ones with brackets in them
drug_names = driver.find_elements_by_xpath('//*[@id="content"]/div/ul[2]')
drug_list = []
for drug in drug_names:
    # print(drug.text)
    drug_list = (drug.text.split('\n'))

# Once we have the list we can start our process
# creating list for the dictionaries we create for each query
dd = []
for drug_name in drug_list: # looping over list of terms we obtained from the page
    dic = {}
    try:
        driver.get(base_link + drug_name + '.html')
        avoid_if = driver.find_element_by_xpath('//*[@id="content"]/div/ul[2]')
        info = driver.find_element_by_xpath('//*[@id="content"]/div/p[3]')
        dic['information'] = info.text.split('\n')
        dic['Generic_name'] = driver.find_element_by_xpath('//*[@id="content"]/div/p[1]/a[1]').text # for getting generic names for drugs we are scraping information.
        dic['drug_class'] = driver.find_element_by_xpath('//*[@id="content"]/div/p[1]/a[2]').text 
        dic['drug_name'] = drug_name
        dic['avoid_if'] = avoid_if.text.split('\n')
        side_effs = driver.find_element_by_xpath('//*[@id="content"]/div/ul[3]')
        dic['side_effects'] = side_effs.text.split('\n')
        usual_dose = driver.find_element_by_xpath('//*[@id="content"]/div/p[28]')
        dic['usual_dose'] = usual_dose.text.split('\n')
        dd.append(dic)
    except:
        print('information not found!')
          
 
driver.quit()

# saving data in json format 
with open('drugs.json', 'w') as f:
    # dump the dictionary object to the file
    json.dump(dd, f)    