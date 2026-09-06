from django.conf import settings
from django.shortcuts import render

from .forms import BirthChartForm
from .services import calculate_birth_chart


# display the birth chart form and calculate after valid submission
def index(request):

    return render(request, 'astrology/index.html',{
        'geoapify_api_key': settings.GEOAPIFY_API_KEY,
        })

def chart(request):
    if request.method == 'POST':
        form = BirthChartForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            # if birth time is empty this becomes None is not None == False
            # if birth time exists this is time object is not None == True
            has_birth_time = data['birth_time'] is not None
            chart = calculate_birth_chart(
                data,
                data['birth_timezone']
            )
            return render(request, 'astrology/chart.html', {
                'chart': chart, 
                'has_birth_time': has_birth_time
                })
    else: 
        form = BirthChartForm()
        return render(request, 'astrology/index.html',{
            'form': form,
            'geoapify_api_key': settings.GEOAPIFY_API_KEY,
            })
    
