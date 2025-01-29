from nlp.query_processor import QueryProcessor
from scrapers.web_scraper import EduScraper
from django.db import transaction
from main.models import EducationalResource

class EduSearchPipeline:
    def __init__(self):
        self.query_processor = QueryProcessor()
        self.scraper = EduScraper()
    
    @transaction.atomic
    def execute_search(self, raw_query):
        """End-to-end search pipeline"""
        # 1. Process query
        processed = self.query_processor.process_query(raw_query)
        
        # 2. Scrape platforms
        scraped_data = self.scraper.scrape_all(processed['processed'])
        
        # 3. Transform & Save
        resources = []
        for platform, items in scraped_data.items():
            for item in items:
                resources.append(
                    EducationalResource(
                        title=item['title'],
                        url=item['url'],
                        content=item['description'],
                        source=platform,
                        resource_type=self._determine_type(platform, item),
                        keywords=processed['semantic_terms']
                    )
                )
        
        # 4. Bulk create and index
        EducationalResource.objects.bulk_create(resources)
        return processed, resources
    
    def _determine_type(self, platform, item):
        """Map platform to resource type"""
        type_map = {
            'YouTube': 'video',
            'Coursera': 'course',
            'edX': 'course',
            'Udemy': 'course'
        }
        return type_map.get(platform, 'other')