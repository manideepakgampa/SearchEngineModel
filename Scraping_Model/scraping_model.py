from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import threading

# List of websites and their respective element details for scraping
websites = [
    {
        "name": "Coursera",
        "url": "https://www.coursera.org/courses/?query=python",
        "element": {"by": By.CLASS_NAME, "value": "rc-DesktopSearchCard"}
    },
    {
        "name": "YouTube",
        "url": "https://www.youtube.com/results?search_query=python+tutorial",
        "element": {"by": By.ID, "value": "video-title"}
    },
    {
        "name": "edX",
        "url": "https://www.edx.org/search?tab=python&page=1",
        "element": {"by": By.CLASS_NAME, "value": "course-card-name"}
    },
    {
        "name": "Udemy",
        "url": "https://www.udemy.com/courses/search/?q=python",
        "element": {"by": By.CLASS_NAME, "value": "course-card--course-title"}
    }
]

# Set up Chrome options to modify the user-agent
options = Options()
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Initialize the browser with multiple tabs and custom user-agent
driver = webdriver.Chrome(options=options)

# Open all websites in separate tabs
driver.get(websites[0]["url"])  # Open the first website
for site in websites[1:]:
    driver.execute_script(f"window.open('{site['url']}');")  # Open other sites in new tabs
time.sleep(3)  # Allow tabs to load

# Get all tab handles (this is done after all tabs are open)
tabs = driver.window_handles

def scrape_tab(index, site):
    """Function to scrape data from a specific tab."""
    driver.switch_to.window(tabs[index])
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
def real_time_scraping():
    for index, site in enumerate(websites):
        scrape_tab(index, site)  # Use index to reference the correct tab

# Thread for real-time scraping
scraping_thread = threading.Thread(target=real_time_scraping)
scraping_thread.start()

print("All tabs are open. You can interact with the browser.")
print("Close the browser window when done.")

# Graceful exit handling
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nClosing browser...")
    driver.quit()
    scraping_thread.join()
