from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import threading
import time

# Website details for scraping
websites = [
    {"name": "Coursera", "url": "https://www.coursera.org/courses/?query=", "element": {"by": By.CLASS_NAME, "value": "rc-DesktopSearchCard"}},
    {"name": "YouTube", "url": "https://www.youtube.com/results?search_query=", "element": {"by": By.ID, "value": "video-title"}},
    {"name": "edX", "url": "https://www.edx.org/search?tab=python&page=1&query=", "element": {"by": By.CLASS_NAME, "value": "course-card-name"}},
    {"name": "Udemy", "url": "https://www.udemy.com/courses/search/?q=", "element": {"by": By.CLASS_NAME, "value": "course-card--course-title"}}
]

# Setup Chrome options
options = Options()
options.add_argument("user-agent=Mozilla/5.0")

def scrape_website(driver, site, query):
    """Scrapes the given website for the provided query."""
    url = site["url"] + query.replace(" ", "+")
    driver.execute_script(f"window.open('{url}', '_blank');")
    driver.switch_to.window(driver.window_handles[-1])
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((site["element"]["by"], site["element"]["value"]))
        )
        elements = driver.find_elements(site["element"]["by"], site["element"]["value"])
        data = [element.text.strip() for element in elements[:10]]
    except Exception as e:
        data = f"Error scraping {site['name']}: {e}"
    
    # Close the current tab
    driver.close()
    # Switch back to the first tab
    driver.switch_to.window(driver.window_handles[0])
    
    return data

def scrape_all_websites(query):
    """Scrapes all websites for the provided query."""
    results = {}
    threads = []
    driver = webdriver.Chrome(options=options)

    def scrape(site):
        results[site["name"]] = scrape_website(driver, site, query)

    for site in websites:
        thread = threading.Thread(target=scrape, args=(site,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Do not quit the driver here to keep the browser window open
    # driver.quit()
    return results