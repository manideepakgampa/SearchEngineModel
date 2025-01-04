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

# Initialize the driver
driver = webdriver.Chrome()

# Iterate over each website
for site in websites:
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
    
    print("-" * 50)

# Close the driver
driver.quit()
