''' 
Script Information
---------------------
Description: 
    This script scrapes the schedule of a class from the Hanze University website.
    
Author: 
    Tom

Date: 
    2021-10-06

Version: 
    1.0

# Usage
-------
Usage: 
    python temptest.py

# Notes
-------
- **Disclaimer**: This script is for educational purposes only. Use at your own risk.
  
- **Required Packages**: 
    - pandas
    - selenium
    - webdriver_manager
    - beautifulsoup4
  
- **Browser Requirements**: 
    - Microsoft Edge browser must be installed.
    - Microsoft Edge WebDriver must be installed and up-to-date.
    - Microsoft Edge WebDriver must be in the PATH environment variable.
    - Microsoft Edge WebDriver must be compatible with the installed Microsoft Edge browser.
'''

# Imports--------------------------------------------------------------
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import pandas as pd
from bs4 import BeautifulSoup
import time
import os
from collections import namedtuple

# Constants------------------------------------------------------------
URL = "https://digirooster.hanze.nl/"
SLEEP_TIME = 1
CLASS = ['23/24 ITV2N1', '23/24 ITV1A', '23/24 ITV1B', '23/24 ITV1C', '23/24 ITV1D', '23/24 ITV1E', '23/24 ITV1F', '23/24 ITV1G', '23/24 ITV1H']
YEARS = ['2', '1', '1', '1', '1', '1', '1', '1', '1', '1']
BColors = namedtuple('BColors', ['HEADER', 'OKBLUE', 'OKCYAN', 'OKGREEN', 'WARNING', 'FAIL', 'ENDC', 'BOLD', 'UNDERLINE'])
bcolors = BColors('\033[95m', '\033[94m', '\033[96m', '\033[92m', '\033[93m', '\033[91m', '\033[0m', '\033[1m', '\033[4m')

# Functions------------------------------------------------------------
def print_green(text):
    print(f"{bcolors.OKGREEN}{text}{bcolors.ENDC}")


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def sleep():
    time.sleep(SLEEP_TIME)

def dottedline():
    """Prints a dotted line that is as long as the console width."""
    print("")
    print_green('-' * pd.get_option('display.width'))
    print("")

def scrape_class_schedule(driver, clas, year):
    driver.get(URL)
    sleep()
    

    year_element = driver.find_element("xpath", "//select[@id='data-selector-year']")
    year_element.click()
    year_element.send_keys(year)
    year_element.click()

    group = driver.find_element("xpath", "//select[@id='data-selector-group']")
    group.click()
    group.send_keys(clas)
    group.click()

    sleep()

    rooster = driver.find_element("xpath", "//div[@class='day-columns']")
    html_content = rooster.get_attribute("innerHTML")

    soup = BeautifulSoup(html_content, 'html.parser')

    for day_div in soup.find_all(class_='day-column'):
        day_label = day_div.find(class_='day-label').text
        date_label = day_div.find(class_='date-label').text

        # Skip Saturday and Sunday
        if day_label in ['Sa', 'Su']:
            continue

        print_green(f"{day_label} {date_label}:")

        for appointment in day_div.find_all(class_='appointment'):
            time = appointment.find(class_='time').text
            subject = appointment.find(class_='subject').text
            location_element = appointment.find(class_='location')
            location = location_element.text if location_element else 'No location'

            print_green(f"  {time} - {subject} ({location})")

        print()

options = Options()
options.add_experimental_option("detach", True)

clear_console()

with webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options) as driver:
    for clas, year in zip(CLASS, YEARS):
        dottedline()
        print(f"{bcolors.HEADER}{bcolors.UNDERLINE}{clas}{bcolors.ENDC}")
        scrape_class_schedule(driver, clas, year)
        dottedline()

