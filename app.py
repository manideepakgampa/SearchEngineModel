from selenium import webdriver
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

# Iterate over each website
for site in websites:
    # Initialize the driver for each website
    driver = webdriver.Chrome()
    print(f"Accessing {site['name']}...")

    # Open the website
    driver.get(site["url"])
    time.sleep(3)  # Allow the page to load

    try:
        # Fetch the page source using Selenium
        page_source = driver.page_source

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Extract elements based on the specified details
        elements = soup.find_all(site["element"]["by"].lower(), class_=site["element"]["value"] 
                                 if site["element"]["by"] == By.CLASS_NAME else None)

        print(f"{site['name']} - Found {len(elements)} items:")
        
        # Print the text of the elements (limit to avoid clutter)
        for idx, element in enumerate(elements[:10]):  # Print only the first 10 items
            print(f"{idx + 1}: {element.text.strip()}")
    except Exception as e:
        print(f"Error accessing {site['name']}: {e}")

    # Close the browser after processing
    driver.quit()
    print(f"{site['name']} completed.")
    print("-" * 50)
