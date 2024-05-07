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
from selenium.webdriver.support.ui import Select

# Constants
URL = "https://digirooster.hanze.nl/"

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
        except Exception as e:
            print(f"Failed to setup webdriver: {e}")
            raise

class HanzeScraper:
    def __init__(self):
        self.driver = None

    def run(self):
        try:
            self.driver = WebDriverManager.setup_driver()
            self.get_page_html()
            self.find_weeks()
            time.sleep(2)

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        finally:
            if self.driver:
                self.driver.quit()

    def get_page_html(self):
        try:
            # Load the page
            self.driver.get(URL)

            # Wait for JavaScript to run
            time.sleep(5)  # Adjust this value as needed

            # Get the page HTML
            page_html = self.driver.page_source
            #print(page_html)

        except Exception as e:
            print(f"Error getting page HTML: {e}")
    
    def find_weeks(self):
        
        from bs4 import BeautifulSoup
    
        # Get the page HTML
        page_html = self.driver.page_source
    
        # Parse the HTML with BeautifulSoup
        soup = BeautifulSoup(page_html, 'html.parser')
    
        # Find the select element by its id
        select_element = soup.find('select', {'id': 'data-selector-range'})
    
        # Find all option elements within the select element
        options = select_element.find_all('option')
        current_week = options[2].text
        print ("Current week: ", current_week)
    
        # Print the text of each option with a number
        print("Possible selections:")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option.text}")
    
        # Prompt the user to enter the number of the week they want to select
        selected_week_number = int(input("Enter the number of the week you want to select: "))
        selected_week = options[selected_week_number - 1].text  # Subtract 1 because list indices start at 0
    
        # Calculate the number of clicks needed
        clicks_needed = 3 - selected_week_number   # Subtract 3 because the current week is the third option
        print(clicks_needed)
        # Determine the direction of the clicks
        if clicks_needed < 0:
            direction = "right"
        else:
            direction = "left"
    
        # Print the number of clicks and the direction
        print(f"Number of clicks needed: {abs(clicks_needed)}")
        print(f"Direction: {direction}")

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
        #----------------------------------------------

        # year selection
        # Find the select element by its id
        select_element = soup.find('select', {'id': 'data-selector-year'})
    
        # Find all option elements within the select element
        options = select_element.find_all('option')
        print("Possible selections:")
        for i, option in enumerate(options, start=1):
            print(f"{i}. Year: {option.text}")
        selected_year_number = int(input("Enter the number of the year you want to select: "))
        selected_year = options[selected_year_number - 1].text
        print(selected_year)
        year_element = self.driver.find_element("xpath", "//select[@id='data-selector-year']")
        year_element.click()
        year_element.send_keys(selected_year)
        year_element.click()

        


        # group selection
        select_element = soup.find('select', {'id': 'data-selector-group'})
        options = select_element.find_all('option')
        print("Possible selections:")
        for i, option in enumerate(options, start=1):
            print(f"{i}. Group: {option.text}")
        selected_group_number = int(input("Enter the number of the group you want to select: "))
        selected_group = options[selected_group_number - 1].text
        print(selected_group)
        group = self.driver.find_element("xpath", "//select[@id='data-selector-group']")
        group.click()
        group.send_keys(selected_group)
        group.click()

        time.sleep(5)
        

        # Return the HTML
        return page_html_after_clicks



if __name__ == "__main__":
    scraper = HanzeScraper()
    scraper.run()
