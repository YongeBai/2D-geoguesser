from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Search
from .forms import SearchForm
import requests
import json
import folium
import geocoder

# Create your views here.


def spell_check(address='ON, Canada'):
    api_key = 'AIzaSyD_LHCw8slH2Tiq7045sjQ8JNoxuoHyQtM'
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json'

    payload = dict()
    payload['address'] = address
    payload['key'] = api_key

    r = requests.get(serviceurl, params=payload)
    data = r.text

    try:
        js = json.loads(data)
    except:
        js = None

    location = js['results'][0]['formatted_address']
    print(location)
    return location

def spell_check(address):
    api_key = 'AIzaSyD_LHCw8slH2Tiq7045sjQ8JNoxuoHyQtM'
    serviceurl = 'https://maps.googleapis.com/maps/api/geocode/json'

    payload = dict()
    payload['address'] = address
    payload['key'] = api_key

    r = requests.get(serviceurl, params=payload)
    data = r.text

    try:
        js = json.loads(data)
    except:
        js = None

    location = js['results'][0]['formatted_address']
    return location

def index(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = SearchForm()
    address = Search.objects.all().last()
    loc = spell_check(address)
    location = geocoder.osm(loc)
    lat = location.lat
    lng = location.lng
    if lat == None or lng == None:
        address.delete()
        return HttpResponse('You address input is invalid')

    # Create Map Object
    m = folium.Map(location=[19, -12], zoom_start=2)

    folium.Marker([lat, lng], tooltip='Click for location',
                  popup=loc).add_to(m)
    # Get HTML Representation of Map Object
    m = m._repr_html_()
    context = {
        'm': m,
        'form': form,
    }
    return render(request, 'index.html', context)