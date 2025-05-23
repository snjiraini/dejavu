from django.shortcuts import render

def api_overview(request):
    """
    Render the API overview page
    """
    return render(request, 'fingerprinting/api_overview.html')
