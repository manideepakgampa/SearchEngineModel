from selenium import webdriver
from selenium.webdriver.common.by import By

# Initialize the driver (it will use the path from the environment variables)
driver = webdriver.Chrome()

# Open the Coursera courses page
driver.get('https://www.coursera.org/courses')

# Find the course titles by their class name
courses = driver.find_elements(By.CLASS_NAME, 'course-title')

# Print the course titles
for course in courses:
    print(course.text)

# Close the driver
driver.quit()
