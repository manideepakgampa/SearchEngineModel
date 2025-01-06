from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# List of websites and their respective element details for scraping
websites = [
    {
        "name": "Coursera",
        "url": "https://www.coursera.org/courses",
        "element": {"by": By.CLASS_NAME, "value": "course-title"}
    },
    {
        "name": "YouTube",
        "url": "https://www.youtube.com/",
        "element": {"by": By.TAG_NAME, "value": "a"}  # Example: All links on the homepage
    },
    {
        "name": "edX",
        "url": "https://www.edx.org/",
        "element": {"by": By.CLASS_NAME, "value": "course-card-name"}  # Example: Course names
    },
    {
        "name": "Udemy",
        "url": "https://www.udemy.com/",
        "element": {"by": By.TAG_NAME, "value": "h2"}  # Example: Section headings
    }
]

# Setup WebDriver with options to keep all tabs in the same browser window
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

# Open all websites in separate tabs
print("Opening all websites in separate tabs...")
for idx, site in enumerate(websites):
    if idx == 0:
        # Open the first website in the initial tab
        driver.get(site["url"])
    else:
        # Open the rest of the websites in new tabs
        driver.execute_script(f"window.open('{site['url']}', '_blank');")
    time.sleep(2)  # Allow tabs to load

print("All tabs are open. You can manually switch between tabs to inspect them.")

try:
    while True:
        print("\n--- Browser Control ---")
        print("1. Close a specific tab manually.")
        print("2. Close the entire browser to exit.")
        print("Waiting for your actions...")

        # Keep the script running until the browser is manually closed
        time.sleep(5)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    print("Closing the browser...")
    driver.quit()
