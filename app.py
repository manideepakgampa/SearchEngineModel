from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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

# Setup WebDriver with options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

# Open the first website in the initial tab
driver.get(websites[0]["url"])
print(f"Opening {websites[0]['name']}...")

# Open the remaining websites in new tabs
for site in websites[1:]:
    driver.execute_script(f"window.open('{site['url']}', '_blank');")
    print(f"Opening {site['name']}...")

print("\nAll websites are now open in separate tabs. You can manually navigate between them.")
print("Close the browser window to exit the script.")

# Keep the script running until the browser window is closed
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    driver.quit()
