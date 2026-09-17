from django.conf import settings
from django.shortcuts import render
from .forms import BirthChartForm
from .services import calculate_birth_chart, generate_chart_svg
from .chatbot import build_chart_context, ask_chart_guide

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
            # determine is user provided birth time
            # if birth time is empty this becomes None is not None == False
            # if birth time exists this is time object is not None == True
            has_birth_time = data['birth_time'] is not None
            chart = calculate_birth_chart(
                data,
                data['birth_timezone']
            )

            # store the calculated chart information so later
            # chatbot requests can use it.
            request.session["chart_context"] = build_chart_context(
                chart,
                has_birth_time,
            )

            # generating a new chart starts a new conversation.
            request.session["chat_history"] = []

            chart_svg = generate_chart_svg(chart, show_houses=has_birth_time)

            return render(request, 'astrology/chart.html', {
                'chart': chart,
                'chart_svg': chart_svg,
                'has_birth_time': has_birth_time
                })
    else: 
        form = BirthChartForm()
        # display the form for a get request, or redisplay it with
        # validation errors after an unsuccessful submission
        return render(request, 'astrology/index.html',{
            'form': form,
            'geoapify_api_key': settings.GEOAPIFY_API_KEY,
            })
    
