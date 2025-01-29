from .coursera_scraper import CourseraScraper
from .youtube_scraper import YouTubeScraper

class EduScraper:
    def __init__(self):
        self.scrapers = {
            'coursera': CourseraScraper(),
            'youtube': YouTubeScraper()
        }

    def scrape(self, query):
        results = []
        for source, scraper in self.scrapers.items():
            try:
                results.extend(scraper.execute(query))
            except Exception as e:
                print(f"Scraping failed for {source}: {str(e)}")
        return results