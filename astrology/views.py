from django.conf import settings
from django.shortcuts import render

from .forms import BirthChartForm


def index(request):
    if request.method == "POST":
        form = BirthChartForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            # Next: pass this validated data to the chart service.
    else:
        form = BirthChartForm()

    return render(request, "astrology/index.html", {
        "form": form,
        "geoapify_api_key": settings.GEOAPIFY_API_KEY,
    })