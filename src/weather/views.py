import requests
from django.shortcuts import render, redirect
from .models import City
from .forms import CityForm

def home(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=215c56eaf790fe95b96935fa3342cbe5'

    err_msg = ''
    msg = ''
    msg_class = ''

    if request.method == 'POST':
        form = CityForm(request.POST or None)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            duplicate_city = City.objects.filter(name=new_city).count()
            if duplicate_city == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err_msg = "City Doesn't Exists in the world!!"
            else:
                err_msg = 'City is Already added!!'
        if err_msg:
            msg = err_msg
            msg_class = 'is-danger'
        else:
            msg = 'City has been added!'
            msg_class = 'is-success'
    else:
        form = CityForm()

    record_weather = []

    cities = City.objects.all()
    for city in cities:
        r = requests.get(url.format(city)).json()
        report = {
            'city': city.name,
            'temp' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
        }

        record_weather.append(report)
    #print(msg)
    args = {
        'record_weather': record_weather,
        'form': form,
        'msg': msg,
        'msg_class' : msg_class
    }
    return render(request, 'weather/weather.html', args)


def delete_city(request, city_name): 
    City.objects.get(name=city_name).delete()
    return redirect('home')