### scraping_model.py

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# List of websites and their respective element details for scraping
websites = [
    {
        "name": "Coursera",
        "url": "https://www.coursera.org/courses/?query=",
        "element": {"by": By.CLASS_NAME, "value": "rc-DesktopSearchCard"}
    },
    {
        "name": "YouTube",
        "url": "https://www.youtube.com/results?search_query=",
        "element": {"by": By.ID, "value": "video-title"}
    },
    {
        "name": "edX",
        "url": "https://www.edx.org/search?tab=python&page=1",
        "element": {"by": By.CLASS_NAME, "value": "course-card-name"}
    },
    {
        "name": "Udemy",
        "url": "https://www.udemy.com/courses/search/?q=",
        "element": {"by": By.CLASS_NAME, "value": "course-card--course-title"}
    }
]

# Set up Chrome options to modify the user-agent
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

def initialize_driver():
    """Initialize the Selenium WebDriver."""
    driver = webdriver.Chrome(options=options)
    return driver

def open_tabs(driver, query):
    """Open all websites with the search query in separate tabs."""
    driver.get(websites[0]["url"] + query)  # Open the first website
    for site in websites[1:]:
        driver.execute_script(f"window.open('{site['url'] + query}');")  # Open other sites in new tabs
    time.sleep(3)  # Allow tabs to load

    return driver.window_handles

def scrape_tab(driver, tab, site):
    """Scrape data from a specific tab."""
    driver.switch_to.window(tab)
    print(f"Scraping {site['name']}...")

    try:
        # Wait for the relevant elements to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((site["element"]["by"], site["element"]["value"]))
        )

        # Scrape the course titles or relevant content
        elements = driver.find_elements(site["element"]["by"], site["element"]["value"])
        print(f"{site['name']} - Found {len(elements)} items:")
        for idx, element in enumerate(elements[:10]):  # Print only the first 10 items
            print(f"{idx + 1}: {element.text.strip()}")
    except Exception as e:
        print(f"Error scraping {site['name']}: {e}")

# Real-time scraping on each tab
def real_time_scraping(driver, tabs):
    for index, site in enumerate(websites):
        scrape_tab(driver, tabs[index], site)
