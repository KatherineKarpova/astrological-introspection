from django.conf import settings
from django.shortcuts import render

def index(request):
    return render(request, "astrology/index.html", {
        "geoapify_api_key": settings.GEOAPIFY_API_KEY,
    })