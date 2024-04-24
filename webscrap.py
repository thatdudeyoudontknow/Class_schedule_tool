import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup

def sleep():
    time.sleep(3)


def get_schedule(driver, year, group):
    sleep()
    # Select year
    year_dropdown = driver.find_element("xpath", "//select[@id='data-selector-year']")
    year_dropdown.click()
    year_dropdown.send_keys(str(year))
    year_dropdown.click()

    # Select group
    group_dropdown = driver.find_element("xpath", "//select[@id='data-selector-group']")
    group_dropdown.click()
    group_dropdown.send_keys(group)
    group_dropdown.click()

    

    rooster = driver.find_element("xpath", "//div[@class='day-columns']")
    html_content = rooster.get_attribute("innerHTML")

    # Parse the HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Iterate through each day column
    for day_div in soup.find_all(class_='day-column'):
        # Extract day label and date
        day_label = day_div.find(class_='day-label').text
        date_label = day_div.find(class_='date-label').text
        
        print(f"{day_label} {date_label}:")
        
        # Iterate through each class (appointment)
        for appointment in day_div.find_all(class_='appointment'):
            time = appointment.find(class_='time').text
            subject = appointment.find(class_='subject').text
            location = appointment.find(class_='location').text
            
            print(f"  {time} - {subject} ({location})")
        
        print()  # Add a new line between days

# Initialize WebDriver
Options = Options()
Options.add_experimental_option("detach", True)
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=Options)
driver.get("https://digirooster.hanze.nl/")
driver.maximize_window()

# Give the site time to load
time.sleep(1)

# Fetch schedule for Year 2 class 23/24 ITV2N1
get_schedule(driver, 2, "23/24 ITV2N1")

# # Fetch schedule for Year 1 (You can add multiple groups for Year 1 as needed)
# year_1_groups = ["23/24 ITV1A", "23/24 ITV1B", "23/24 ITV1C","23/24 ITV1D","23/24 ITV1E","23/24 ITV1F"]

# for group in year_1_groups:
#     get_schedule(driver, 1, group)

# Close the driver
driver.quit()
