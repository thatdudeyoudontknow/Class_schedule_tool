from selenium import webdriver
from selenium.webdriver.edge.service import Service
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import time
from bs4 import BeautifulSoup

# Variable to control headless mode
headless_mode = False

# Setup options for headless browsing
options = webdriver.EdgeOptions()
options.use_chromium = True

# Add incognito argument
options.add_argument("--inprivate")

if headless_mode:
    options.add_argument("--headless")
    options.add_argument("disable-gpu")

# Suppress logging messages
options.add_argument("--log-level=3")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Create a new instance of the Edge driver
driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()), options=options)

# Go to Google's homepage
driver.get("https://digirooster.hanze.nl/")

# Print the page title
print(driver.title)
# Print the entire HTML
html = driver.page_source
print(html)
soup = BeautifulSoup(html, 'html.parser')
inputs = soup.find_all('input')
for i in inputs:
    print(f"Name: {i.get('name')}, ID: {i.get('id')}")

# Find all elements with the specific class
elements = soup.find_all(class_="form-control ltr_override input ext-input text-box ext-text-box")
print('empty spaces')
# Print the name and id of each element
for i in elements:
    print(f"Name: {i.get('name')}, ID: {i.get('id')}")
# Print the current URL
print(driver.current_url)
print ("spaces")



# Close the driver only in headless mode
if headless_mode:
    driver.quit()

# Keep the script running if not in headless mode
if not headless_mode:
    while True:
        pass