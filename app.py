from selenium import webdriver
from selenium.webdriver.common.by import By
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

# Iterate over each website
for site in websites:
    # Initialize the driver for each website
    driver = webdriver.Chrome()
    print(f"Accessing {site['name']}...")
    
    # Open the website
    driver.get(site["url"])
    time.sleep(3)  # Allow the page to load
    
    try:
        # Find the elements based on specified locator
        elements = driver.find_elements(site["element"]["by"], site["element"]["value"])
        print(f"{site['name']} - Found {len(elements)} items:")
        
        # Print text of the elements (limit to avoid clutter)
        for idx, element in enumerate(elements[:10]):  # Print only first 10 items
            print(f"{idx + 1}: {element.text.strip()}")
    except Exception as e:
        print(f"Error accessing {site['name']}: {e}")
    
    print(f"Close the browser window for {site['name']} to continue to the next site...")
    
    # Wait until the browser window is closed
    while True:
        try:
            driver.title  # Try accessing the driver; if it's closed, an exception will occur
            time.sleep(1)
        except:
            break  # Exit the loop when the browser window is closed
    
    print(f"{site['name']} closed. Moving to the next site...")
    print("-" * 50)
