from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, WebDriverException
import pandas as pd
from bs4 import BeautifulSoup
import time
import os
from collections import namedtuple
import json
import datetime

# Constants
URL = "https://digirooster.hanze.nl/"
SLEEP_TIME = 1
#CLASS = ['23/24 ITV2N1', '23/24 ITV1A', '23/24 ITV1B', '23/24 ITV1C', '23/24 ITV1D', '23/24 ITV1E', '23/24 ITV1F', '23/24 ITV1G', '23/24 ITV1H']
#YEARS = ['2', '1', '1', '1', '1', '1', '1', '1', '1', '1']
BColors = namedtuple('BColors', ['HEADER', 'OKGREEN', 'FAIL', 'ENDC'])
bcolors = BColors('\033[95m', '\033[92m', '\033[91m', '\033[0m')

class ConsoleUtils:
    @staticmethod
    def print_green(text):
        print(f"{bcolors.OKGREEN}{text}{bcolors.ENDC}")
    
    def print_purple(text):
        print(f"{bcolors.HEADER}{text}{bcolors.ENDC}")

    @staticmethod
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def dottedline():
        print("")
        ConsoleUtils.print_green('-' * pd.get_option('display.width'))
        print("")

class WebDriverManager:
    @staticmethod
    def setup_driver():
        options = webdriver.EdgeOptions()
        options.add_argument("--log-level=3")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        
        try:
            driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)
            driver.maximize_window()
            return driver
        except WebDriverException as e:
            print(f"{bcolors.FAIL}Failed to setup webdriver: {e}{bcolors.ENDC}")
            raise

class HanzeScraper:
    def __init__(self):
        self.driver = None
        self.years = []
        self.classes = []

    def run(self):
        ConsoleUtils.clear_console()
        ConsoleUtils.dottedline()
        print(f"{bcolors.HEADER}Hanze University Class Schedule Scraper{bcolors.ENDC}")

        try:
            self.driver = WebDriverManager.setup_driver()
            current_week = self.get_current_week()
            
            self.find_weeks()
            self.select_year_and_class()
            time.sleep(SLEEP_TIME)
            for clas, year in zip(self.classes, self.years):
                ConsoleUtils.dottedline()
                print(f"{bcolors.HEADER}{clas}{bcolors.ENDC}")
                self.scrape_class_schedule(clas, year)
                ConsoleUtils.dottedline()

        except NoSuchWindowException:
            print(f"{bcolors.FAIL}The browser window was closed unexpectedly. Please keep the browser window open.{bcolors.ENDC}")

        except NoSuchElementException as e:
            print(f"{bcolors.FAIL}Element not found: {e}{bcolors.ENDC}")

        except WebDriverException as e:
            print(f"{bcolors.FAIL}WebDriver error: {e}{bcolors.ENDC}")

        except Exception as e:
            print(f"{bcolors.FAIL}An unexpected error occurred: {e}{bcolors.ENDC}")

        finally:
            if self.driver:
                self.driver.quit()
            time.sleep(SLEEP_TIME)

    def select_year_and_class(self):
        while True:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # Year selection
            select_element = soup.find('select', {'id': 'data-selector-year'})
            options = select_element.find_all('option')
            ConsoleUtils.print_purple("Possible selections:")
            for i, option in enumerate(options, start=1):
                ConsoleUtils.print_green(f"{i}. Year: {option.text}")
            ConsoleUtils.print_purple("Enter the number of the year you want to select: ")
            selected_year_number = int(input())
            selected_year = options[selected_year_number - 1].text
            year_element = self.driver.find_element("xpath", "//select[@id='data-selector-year']")
            year_element.click()
            year_element.send_keys(selected_year)
            year_element.click()
            self.years.append(selected_year)
            time.sleep(4)
            

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            # Group selection
            select_element = soup.find('select', {'id': 'data-selector-group'})
            options = select_element.find_all('option')
            ConsoleUtils.print_purple("Possible selections:")
            for i, option in enumerate(options, start=1):
                ConsoleUtils.print_green(f"{i}. Group: {option.text}")
            ConsoleUtils.print_purple("Enter the number of the group you want to select: ")
            selected_group_number = int(input())
            selected_group = options[selected_group_number -1].text
            group = self.driver.find_element("xpath", "//select[@id='data-selector-group']")
            group.click()
            group.send_keys(selected_group)
            group.click()
            self.classes.append(selected_group)

            ConsoleUtils.clear_console()
            ConsoleUtils.dottedline()
            print(f"{bcolors.HEADER}Hanze University Class Schedule Scraper{bcolors.ENDC}")

            # Ask user if they want to add another year/class
            ConsoleUtils.print_purple("Do you want to add another year/class? (yes/no): ")
            add_more = input()
            ConsoleUtils.clear_console()
            ConsoleUtils.dottedline()
            print(f"{bcolors.HEADER}Hanze University Class Schedule Scraper{bcolors.ENDC}")
            print ("")
            if add_more.lower() != 'yes':
                break


    def find_weeks(self):
        # Get the page HTML
        page_html = self.driver.page_source

        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(page_html, 'html.parser')

        # Find the select element by its id
        select_element = soup.find('select', {'id': 'data-selector-range'})

        # Find all option elements within the select element
        options = select_element.find_all('option')
        current_week = options[2].text
        

        # Print the text of each option with a number
        ConsoleUtils.print_purple("Possible weeks:")
        for i, option in enumerate(options, start=1):
            ConsoleUtils.print_green(f"{i}. {option.text}")

        # Prompt the user to enter the number of the week they want to select
        ConsoleUtils.print_purple("Enter the number of the week you want to select: ")
        selected_week_number = int(input())
        selected_week = options[selected_week_number - 1].text  # Subtract 1 because list indices start at 0

        # Calculate the number of clicks needed
        clicks_needed = 3-selected_week_number   # Subtract 3 because the current week is the third option

        # Determine the direction of the clicks
        if clicks_needed < 0:
            direction = "right"
        else:
            direction = "left"

        

        # Find the button and click it the necessary number of times
        if direction == "right":
            button = self.driver.find_element("xpath", '//button[@data-period="next"]')
        else:
            button = self.driver.find_element("xpath", '//button[@data-period="prev"]')

        for _ in range(abs(clicks_needed)):
            button.click()
            time.sleep(1)  # Wait for the page to load after each click

        # Get the page HTML after the clicks
        page_html_after_clicks = self.driver.page_source
        
        ConsoleUtils.clear_console()
        ConsoleUtils.dottedline()
        print(f"{bcolors.HEADER}Hanze University Class Schedule Scraper{bcolors.ENDC}")
        print("")

    def get_current_week(self):
        try:
            self.driver.get(URL)
            
            #wait for the page to load
            time.sleep(SLEEP_TIME)
            #print all the options with the id data-selector-range
            all_weeks = self.driver.find_elements(by="xpath",value= "//select[@id='data-selector-range']/option")


            # from all the weeks with start of week and end of week, find the current week by comparing the current date
            current_date = datetime.datetime.now().date()
            for i, week in enumerate(all_weeks, start=1):
                week_info = week.get_attribute('innerHTML')
                week_value = week.get_attribute('value')
                week_value_json = json.loads(week_value)
                start_date = datetime.datetime.strptime(week_value_json['start'].split('T')[0], '%Y-%m-%d').date()
                end_date = datetime.datetime.strptime(week_value_json['end'].split('T')[0], '%Y-%m-%d').date()
                if start_date <= current_date <= end_date:
                    current_week = week_info
                    ConsoleUtils.print_green(f"Current week: {current_week}")
                    break




        except NoSuchElementException as e:
            print(f"{bcolors.FAIL}Error fetching current week: {e}{bcolors.ENDC}")
            raise

    def scrape_class_schedule(self, clas, year):
        try:
            
            self.set_year_and_class(clas, year)
            rooster_html = self.get_rooster_html()
            self.parse_rooster(rooster_html)

        except NoSuchElementException as e:
            print(f"{bcolors.FAIL}Error scraping class schedule: {e}{bcolors.ENDC}")

    def set_year_and_class(self, clas, year):
        try:
            year_element = self.driver.find_element("xpath", "//select[@id='data-selector-year']")
            year_element.click()
            year_element.send_keys(year)
            year_element.click()

            group = self.driver.find_element("xpath", "//select[@id='data-selector-group']")
            group.click()
            group.send_keys(clas)
            group.click()
            time.sleep(SLEEP_TIME)

        except NoSuchElementException as e:
            print(f"{bcolors.FAIL}Error setting year and class: {e}{bcolors.ENDC}")

    def get_rooster_html(self):
        try:
            rooster = self.driver.find_element("xpath", "//div[@class='day-columns']")
            return rooster.get_attribute("innerHTML")

        except NoSuchElementException as e:
            print(f"{bcolors.FAIL}Error fetching class schedule HTML: {e}{bcolors.ENDC}")
            raise

    def parse_rooster(self, html_content):
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            for day_div in soup.find_all(class_='day-column'):
                day_label = day_div.find(class_='day-label').text
                date_label = day_div.find(class_='date-label').text

                if day_label in ['Sa', 'Su']:
                    continue

                ConsoleUtils.print_green(f"{day_label} {date_label}:")

                for appointment in day_div.find_all(class_='appointment'):
                    time = appointment.find(class_='time').text
                    subject = appointment.find(class_='subject').text
                    location_element = appointment.find(class_='location')
                    location = location_element.text if location_element else 'No location'

                    ConsoleUtils.print_green(f"  {time} - {subject} ({location})")

        except Exception as e:
            print(f"{bcolors.FAIL}Error parsing class schedule: {e}{bcolors.ENDC}")

if __name__ == "__main__":
    scraper = HanzeScraper()
    scraper.run()
