from django.shortcuts import render

def main_page(request):
    return render(request, 'main_page.html')

def search_page(request):
    query = request.GET.get('q', '')
    filter_type = request.GET.get('type', '')
    filter_subject = request.GET.get('subject', '')
    min_price = request.GET.get('min_price', '0')
    max_price = request.GET.get('max_price', '100')

    # Mock search results (replace with actual database queries)
    all_results = [
        {'title': 'Dark Chocolate', 'price': 3.49, 'type': 'Textbook', 'subject': 'Che'},
        {'title': 'Milk Chocolate', 'price': 0.69, 'type': 'Practice Test', 'subject': 'Bio'},
        {'title': 'White Chocolate', 'price': 3.49, 'type': 'Online', 'subject': 'Phy'},
        {'title': 'Cocoa Chocolate', 'price': 0.89, 'type': 'Paid', 'subject': 'Mat'},
    ]

    # Apply filters
    results = [
        result for result in all_results
        if (not filter_type or result['type'] == filter_type) and
           (not filter_subject or result['subject'] == filter_subject) and
           float(min_price) <= result['price'] <= float(max_price)
    ]

    return render(request, 'search_page.html', {
        'query': query,
        'results': results,
        'filters': {
            'type': filter_type,
            'subject': filter_subject,
            'min_price': min_price,
            'max_price': max_price,
        }
    })
