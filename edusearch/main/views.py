# Project-1/edusearch/main/views.py
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage
from elasticsearch_dsl import Search, Q
# from .search_indexes import EducationalResourceIndex
# from .nlp.query_analyzer import get_bert_embeddings  # Your NLP module
import math

RESULTS_PER_PAGE = 8

def main_page(request):
    """Render homepage with AI search interface"""
    return render(request, 'main_page.html')

def search_page(request):
    """Advanced search results with ElasticSearch integration"""
    # Get search query and filters
    query = request.GET.get('q', '')
    resource_type = request.GET.getlist('type', [])
    min_price = request.GET.get('min_price', '0')
    max_price = request.GET.get('max_price', '1000')
    difficulty = request.GET.get('difficulty', '')
    page_number = request.GET.get('page', 1)
    
    try:
        # Initialize ElasticSearch query
        search = Search(index='educational_resources')
        
        # Basic match query with boost
        if query:
            search = search.query(
                Q('multi_match', query=query, 
                  fields=['title^3', 'content^2', 'description'])
            )
            
        # Filter by price range
        search = search.filter(
            'range', price={'gte': min_price, 'lte': max_price}
        )
        
        # Filter by resource type
        if resource_type:
            search = search.filter('terms', resource_type=resource_type)
            
        # Filter by difficulty
        if difficulty:
            search = search.filter('term', difficulty=difficulty)
            
        # Add aggregations for filter counts
        search.aggs.bucket('resource_types', 'terms', field='resource_type') \
                  .bucket('difficulty_levels', 'terms', field='difficulty')
        
        # Pagination
        start = (int(page_number) - 1) * RESULTS_PER_PAGE
        search = search[start:start + RESULTS_PER_PAGE]
        
        # Execute search
        response = search.execute()
        
        # Process results
        results = [{
            'title': hit.title,
            'description': hit.content[:200] + '...' if hit.content else '',
            'price': hit.price,
            'resource_type': hit.resource_type,
            'difficulty': hit.difficulty,
            'source': hit.source,
            'url': hit.url,
            'is_free': hit.price == 0
        } for hit in response]
        
        # Get filter aggregations
        resource_types_agg = {
            bucket.key: bucket.doc_count 
            for bucket in response.aggregations.resource_types.buckets
        }
        
        # Generate AI recommendations (simplified example)
        ai_recommendations = generate_ai_recommendations(query)
        
        # Pagination setup
        total_results = response.hits.total.value
        total_pages = math.ceil(total_results / RESULTS_PER_PAGE)
        
    except Exception as e:
        results = []
        resource_types_agg = {}
        ai_recommendations = []
        total_pages = 1
    
    return render(request, 'search_page.html', {
        'query': query,
        'results': results,
        'filters': {
            'resource_types': [
                {'value': 'course', 'label': 'Courses', 'count': resource_types_agg.get('course', 0)},
                {'value': 'tutorial', 'label': 'Tutorials', 'count': resource_types_agg.get('tutorial', 0)},
                {'value': 'paper', 'label': 'Research Papers', 'count': resource_types_agg.get('paper', 0)}
            ],
            'min_price': min_price,
            'max_price': max_price,
            'difficulty': difficulty
        },
        'ai_recommendations': ai_recommendations,
        'pagination': {
            'current': int(page_number),
            'total': total_pages,
            'has_prev': int(page_number) > 1,
            'has_next': int(page_number) < total_pages,
        }
    })

def generate_ai_recommendations(query):
    """Generate AI-powered search suggestions using NLP"""
    # Example implementation using BERT embeddings
    if not query:
        return []
    
    # Get semantic embeddings
    embeddings = get_bert_embeddings(query)
    
    # Example recommendations (replace with actual ML model)
    return [
        f'Try "{query} for beginners"',
        f'Free resources about {query}',
        f'Advanced courses in {query}'
    ]