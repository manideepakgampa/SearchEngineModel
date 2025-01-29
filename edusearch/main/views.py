from django.shortcuts import render
from .models import EducationalResource
from .scrapers import EduScraper
from .nlp import QueryProcessor

def main_page(request):
    return render(request, 'main/main_page.html')

def search_page(request):
    query = request.GET.get('q', '')
    processor = QueryProcessor()
    scraper = EduScraper()
    
    # Process query
    analysis = processor.process(query)
    
    # Scrape and save results
    results = scraper.scrape(analysis['processed_query'])
    EducationalResource.objects.bulk_create([
        EducationalResource(**item) for item in results
    ])
    
    # Get from DB
    resources = EducationalResource.objects.filter(
        search_vector=analysis['processed_query']
    )[:20]
    
    return render(request, 'main/search_page.html', {
        'query': query,
        'results': resources,
        'analysis': analysis
    })