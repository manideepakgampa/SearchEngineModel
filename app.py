import requests
from bs4 import BeautifulSoup

url = 'https://www.coursera.org/courses'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Example: Scrape course titles
courses = soup.find_all('h2', class_='course-title')
for course in courses:
    print(course.get_text())
