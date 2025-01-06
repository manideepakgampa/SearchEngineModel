from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time

# List of websites and their respective URLs
websites = [
    {"name": "Coursera", "url": "https://www.coursera.org/courses"},
    {"name": "YouTube", "url": "https://www.youtube.com/"},
    {"name": "edX", "url": "https://www.edx.org/"},
    {"name": "Udemy", "url": "https://www.udemy.com/"},
]

# Setup WebDriver with options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)

try:
    # Open the first website in the initial tab
    driver.get(websites[0]["url"])
    print(f"Opening {websites[0]['name']}...")

    # Open the remaining websites in new tabs
    for site in websites[1:]:
        driver.execute_script(f"window.open('{site['url']}', '_blank');")
        print(f"Opening {site['name']}...")

    print("\nAll websites are now open in separate tabs. You can manually navigate between them.")
    print("Close the browser window to exit the script.")

    # Keep the script running until the browser is closed
    while True:
        try:
            # Check if the browser is still open
            driver.title
        except WebDriverException:
            print("Browser closed. Exiting script.")
            break
        time.sleep(1)

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Quit the driver if it's still open
    try:
        driver.quit()
    except WebDriverException:
        pass
