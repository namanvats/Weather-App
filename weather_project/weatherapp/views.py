from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm

# Create your views here.


def index(request):
    cities = City.objects.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=b5b09112c857ece338703eaa51f977fe'
    if request.method == 'POST':  # only true if form is submitted
        form = CityForm(request.POST)  # add actual request data to form for processing
        form.save()  # will validate and save if validate
    form = CityForm()
    weather_data = []
    for city in cities:
        city_weather = requests.get(url.format(city)).json()
        weather = {
            'city': city,
            'temperature': city_weather['main']['temp'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }
        weather_data.append(weather)
    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weatherapp/index.html', context)  # returns the index.html template