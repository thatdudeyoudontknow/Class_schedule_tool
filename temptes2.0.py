from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.common.exceptions import NoSuchElementException, NoSuchWindowException, WebDriverException
import pandas as pd
from bs4 import BeautifulSoup
import time
import os
from collections import namedtuple

# Constants
URL = "https://digirooster.hanze.nl/"
SLEEP_TIME = 1
CLASS = ['23/24 ITV2N1', '23/24 ITV1A', '23/24 ITV1B', '23/24 ITV1C', '23/24 ITV1D', '23/24 ITV1E', '23/24 ITV1F', '23/24 ITV1G', '23/24 ITV1H']
YEARS = ['2', '1', '1', '1', '1', '1', '1', '1', '1', '1']
BColors = namedtuple('BColors', ['HEADER', 'OKGREEN', 'FAIL', 'ENDC'])
bcolors = BColors('\033[95m', '\033[92m', '\033[91m', '\033[0m')

class ConsoleUtils:
    @staticmethod
    def print_green(text):
        print(f"{bcolors.OKGREEN}{text}{bcolors.ENDC}")

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

    def run(self):
        ConsoleUtils.clear_console()
        ConsoleUtils.dottedline()
        print(f"{bcolors.HEADER}Hanze University Class Schedule Scraper{bcolors.ENDC}")

        try:
            self.driver = WebDriverManager.setup_driver()
            current_week = self.get_current_week()

            self.find_weeks()
            time.sleep(SLEEP_TIME)
            for clas, year in zip(CLASS, YEARS):
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
        print("Possible selections:")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option.text}")

        # Prompt the user to enter the number of the week they want to select
        selected_week_number = int(input("Enter the number of the week you want to select: "))
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

        # Return the HTML
        return page_html_after_clicks

    def get_current_week(self):
        try:
            self.driver.get(URL)
            week_info = self.driver.find_element("xpath", "//select[@id='data-selector-range']/option[3]").get_attribute("innerHTML")
            parts = week_info.split(' ')
            formatted_week_info = f"{parts[2]} {parts[3]} ({parts[0]} {parts[1]})"
            ConsoleUtils.print_green(f"Current week: {formatted_week_info}")
            return formatted_week_info

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
