from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from urllib.parse import quote_plus
import json

class EduScraper:
    CONFIG = {
        "Coursera": {
            "url": "https://www.coursera.org/courses?query=",
            "selectors": {
                "container": "li.ais-InfiniteHits-item",
                "title": "h2",
                "description": ".description",
                "link": "a::attr(href)"
            }
        },
        "YouTube": {
            "url": "https://www.youtube.com/results?search_query=",
            "selectors": {
                "container": "ytd-video-renderer",
                "title": "#video-title",
                "description": "#description-text",
                "link": "#video-title::attr(href)"
            }
        }
    }

    def __init__(self):
        self.driver = self._init_driver()
        self.wait = WebDriverWait(self.driver, 15)

    def _init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        return webdriver.Chrome(options=options)

    def scrape_all(self, query):
        """Unified scraping interface"""
        results = {}
        for platform, config in self.CONFIG.items():
            try:
                results[platform] = self._scrape_site(
                    config['url'] + quote_plus(query),
                    config['selectors']
                )
            except Exception as e:
                print(f"Error scraping {platform}: {str(e)}")
        return results

    def _scrape_site(self, url, selectors):
        """Generic scraping workflow"""
        self.driver.get(url)
        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, selectors['container'])
        ))
        
        elements = self.driver.find_elements(
            By.CSS_SELECTOR, selectors['container']
        )
        
        return [self._extract_data(element, selectors) 
                for element in elements[:10]]

    def _extract_data(self, element, selectors):
        """Extract structured data from elements"""
        return {
            'title': element.find_element(
                By.CSS_SELECTOR, selectors['title']
            ).text,
            'description': element.find_element(
                By.CSS_SELECTOR, selectors['description']
            ).text,
            'url': element.find_element(
                By.CSS_SELECTOR, selectors['link']
            ).get_attribute('href')
        }

    def __del__(self):
        if self.driver:
            self.driver.quit()