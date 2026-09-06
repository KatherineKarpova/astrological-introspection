from django.conf import settings
from django.shortcuts import render

from .forms import BirthChartForm
from .services import calculate_birth_chart


# display the birth chart form and calculate after valid submission
def index(request):

    chart = None

    print('REQUEST METHOD:', request.method)
    if request.method == 'POST':
        form = BirthChartForm(request.POST)

        print('POST DATA:', request.POST)
        print('FORM BOUND:', form.is_bound)

        if form.is_valid():
            data = form.cleaned_data

            if data['birth_time'] is None:
                form.add_error(
                    'birth_time',
                    'Unknown-time charts are not implemented yet. '
                    'Enter a known birth time for this test.',
                )
            else:
                chart = calculate_birth_chart(
                    data,
                    data['birth_timezone']
                )

                print('Sun:', chart.sun.sign, chart.sun.position)
                print('Moon:', chart.moon.sign, chart.moon.position)
                print(
                    'Ascendant:',
                    chart.ascendant.sign,
                    chart.ascendant.position
                )

    elif request.method == 'GET':
        form = BirthChartForm()
        
        print('FORM BOUND:', form.is_bound)

    print('FORM ERRORS:', form.errors)
    return render(
        request,
        'astrology/index.html',
        {
            'form': form,
            'geoapify_api_key': settings.GEOAPIFY_API_KEY,
            'chart': chart,
        }
    )