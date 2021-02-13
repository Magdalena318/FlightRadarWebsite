from django.shortcuts import render, redirect
from django.http import JsonResponse
from .proxy import get_flight_radar_data
from .models import Plane, Flight, Airport, Waypoint
from django.middleware.csrf import get_token
from django.db.models import Max, Min
import json
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.gis.geos import Polygon
from datetime import datetime
from collections import OrderedDict


def index(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            user = request.user
            account_type = "Admin" if user.is_superuser else "Standard user"
            data = {
                'account_type': account_type,
            }
            response = render(request, 'monitor_auth.html', {'data': data})
        else:
            response = render(request, 'monitor_unauth.html')
    else:
        result = {
            'result': 'Incorrect type of request'
        }
        response = JsonResponse(result, status=400)
    response.set_cookie("csrftoken", get_token(request))
    return response


#Monitoring planes
def planes_data(request):
    if request.method == 'GET':
        lamin = float(request.GET.get('lamin', ''))
        lamax = float(request.GET.get('lamax', ''))
        lomin = float(request.GET.get('lomin', ''))
        lomax = float(request.GET.get('lomax', ''))
        bounds = [lamin, lamax, lomin, lomax]

        data = get_flight_radar_data(bounds)

        response = JsonResponse(data, status=200)
        return response
    else:
        response = JsonResponse('Incorrect type of request', status=400)
        return response

#Lookup staff
def lookup(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = request.user
            account_type = "Admin" if user.is_superuser else "Standard user"
            data = {
                'account_type': account_type,
            }
            response = render(request, 'lookup.html', {'data': data})
        else:
            result = {
                'result': 'Incorrect type of request'
            }
            response = JsonResponse(result, status=400)
    else:
        result = {
            'result': 'You are not authenticated!',
        }
        response = render(request, 'result_unauth.html', {'result': result})
    return response


def lookup_planes(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = request.user
            account_type = "Admin" if user.is_superuser else "Standard user"
            data = {
                'account_type': account_type,
                'max_flight_range': Plane.objects.all().aggregate(Max('flight_range')),
                'min_flight_range': Plane.objects.all().aggregate(Min('flight_range')),
                'max_speed_range': Plane.objects.all().aggregate(Max('speed')),
                'min_speed_range': Plane.objects.all().aggregate(Min('speed')),
                'max_passenger_max': Plane.objects.all().aggregate(Max('max_passenger')),
                'max_passenger_min': Plane.objects.all().aggregate(Min('max_passenger')),
            }
            response = render(request, 'lookup_airplanes.html', {'data': data})
        elif request.method == 'POST':
            json_data = json.loads(request.body)
            planes = Plane.objects.filter(flight_range__lte=json_data['max_flight_range'], flight_range__gte=json_data['min_flight_range'], speed__lte=json_data['max_speed_range'], speed__gte = json_data['min_speed_range'], max_passenger__lte = json_data['max_passenger_max'], max_passenger__gte = json_data['max_passenger_min'])
            planes = planes.filter(name__contains=json_data['name']).order_by('name')
            result = serializers.serialize('json', planes)
            print(result)
            response = JsonResponse(result, content_type='application/json', safe=False, status=200)
        else:
            result = {
                'result': 'Incorrect type of request'
            }
            response = JsonResponse(result, status=400)
    else:
        result = {
            'result': 'You are not authenticated!',
        }
        response = render(request, 'result_unauth.html', {'result': result})
    response.set_cookie("csrftoken", get_token(request))
    return response


def lookup_airports(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            if request.GET.__contains__('country'):
                data = Airport.objects.filter(country=request.GET.__getitem__('country')).exclude(city='').order_by('city').values_list('city', flat=True).distinct()
                print(data)
                data = json.dumps(list(data), cls=DjangoJSONEncoder)
                response = JsonResponse(data, content_type='application/json', safe=False, status=200)
            else:
                user = request.user
                account_type = "Admin" if user.is_superuser else "Standard user"
                data = {
                    'countries': Airport.objects.all().order_by('country').values_list('country', flat=True).distinct(),
                    'account_type': account_type,
                }
                response = render(request, 'lookup_airports.html', {'data': data})
        elif request.method == 'POST':
            json_data = json.loads(request.body)
            airports = Airport.objects.all().order_by('id')
            if json_data['id'] != '':
                airports = airports.filter(id=json_data['id'])
            if json_data['name'] != '':
                airports = airports.filter(name__contains=json_data['name'])
            if json_data['country'] != 'Not selected':
                airports = airports.filter(country__contains=json_data['country'])
            if json_data['city'] != 'Not selected':
                airports = airports.filter(city__contains=json_data['city'])
            min_lat = json_data['min_lat']
            max_lat = json_data['max_lat']
            min_lng = json_data['min_lng']
            max_lng = json_data['max_lng']
            if max_lat != '' and max_lng != '' and min_lat != '' and min_lng != '':
                poly = Polygon(((min_lat, min_lng), (min_lat, max_lng), (max_lat, max_lng), (max_lat, min_lng), (min_lat, min_lng)))
                airports = airports.filter(location__contained=poly)
            result = serializers.serialize('json', airports)
            response = JsonResponse(result, content_type='application/json', safe=False, status=200)
        else:
            result = {
                'result': 'Incorrect type of request'
            }
            response = JsonResponse(result, status=400)
    else:
        result = {
            'result': 'You are not authenticated!',
        }
        response = render(request, 'result_unauth.html', {'result': result})
    response.set_cookie("csrftoken", get_token(request))
    return response

def lookup_flights(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = request.user
            account_type = "Admin" if user.is_superuser else "Standard user"
            data = {
                'account_type': account_type,
                'countries': Airport.objects.all().order_by('country').values_list('country', flat=True).distinct(),
                'cities': Airport.objects.all().order_by('city').exclude(city='').values_list('city',
                                                                                              flat=True).distinct(),
                'airports': Airport.objects.all().order_by('name').values_list('name', flat=True).distinct(),
                'planes': Plane.objects.all().order_by('name').values_list('name', flat=True).distinct(),
            }
            response = render(request, 'lookup_flights.html', {'data': data})
        elif request.method == 'POST':
            json_data = json.loads(request.body)
            flights = Flight.objects.all().order_by('id')
            if json_data['id'] != '':
                flights = flights.filter(id=json_data['id'])

            if json_data['dep_country'] != 'Not selected':
                flights = flights.filter(departure_airport__country__contains=json_data['dep_country'])
            if json_data['dep_city'] != 'Not selected':
                flights = flights.filter(departure_airport__city__contains=json_data['dep_city'])
            if json_data['dep_airport'] != 'Not selected':
                flights = flights.filter(departure_airport__name__contains=json_data['dep_airport'])

            if json_data['arr_country'] != 'Not selected':
                flights = flights.filter(arrival_airport__country__contains=json_data['arr_country'])
            if json_data['arr_city'] != 'Not selected':
                flights = flights.filter(arrival_airport__city__contains=json_data['arr_city'])
            if json_data['arr_airport'] != 'Not selected':
                flights = flights.filter(arrival_airport__name__contains=json_data['arr_airport'])

            if json_data['alt_country'] != 'Not selected':
                flights = flights.filter(alternate_airport__country__contains=json_data['alt_country'])
            if json_data['alt_city'] != 'Not selected':
                flights = flights.filter(alternate_airport__city__contains=json_data['alt_city'])
            if json_data['alt_airport'] != 'Not selected':
                flights = flights.filter(alternate_airport__name__contains=json_data['alt_airport'])

            if json_data['dep_time'] != '':
                flights = flights.filter(departure_time=json_data['dep_time'])
            if json_data['arr_time'] != '':
                flights = flights.filter(arrival_time=json_data['arr_time'])

            result = serializers.serialize('json', flights)
            response = JsonResponse(result, content_type='application/json', safe=False, status=200)
        else:
            result = {
                'result': 'Incorrect type of request'
            }
            response = JsonResponse(result, status=400)
    else:
        result = {
            'result': 'You are not authenticated!',
        }
        response = render(request, 'result_unauth.html', {'result': result})
    response.set_cookie("csrftoken", get_token(request))
    return response


#Flights
def add_flight(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = request.user
            account_type = "Admin" if user.is_superuser else "Standard user"
            data = {
                'account_type': account_type,
                'countries': Airport.objects.all().order_by('country').values_list('country', flat=True).distinct(),
                'cities': Airport.objects.all().order_by('city').exclude(city='').values_list('city',
                                                                                              flat=True).distinct(),
                'airports': Airport.objects.all().order_by('name').values_list('name', flat=True).distinct(),
                'planes': Plane.objects.all().order_by('name').values_list('name', flat=True).distinct(),
            }
            response = render(request, 'add_flight.html', {'data': data})
        elif request.method == 'POST':
            json_data = json.loads(request.body)
            flight = Flight()
            flight.plane = Plane.objects.get(name=json_data['plane'])
            flight.departure_airport = Airport.objects.get(name=json_data['dep_airport'])
            flight.arrival_airport = Airport.objects.get(name=json_data['arr_airport'])
            flight.alternate_airport = Airport.objects.get(name=json_data['alt_airport'])
            flight.departure_time = json_data['dep_time']
            result = flight.calculate_route()
            if result['result'] == 'Success':
                flight.calculate_arrival_time()
                flight.save()
                result = {
                    'result': 'Success',
                    'reason': 'Flight has been submitted successfully!',
                    'id': str(flight.id),
                }
            result = json.dumps(result)
            print(result)
            response = JsonResponse(result, content_type='application/json', safe=False, status=200)
        else:
            result = {
                'result': 'Incorrect type of request'
            }
            response = render(request, 'result_unauth.html', {'result': result})
    else:
        result = {
            'result': 'You are not authenticated!',
        }
        response = render(request, 'result_unauth.html', {'result': result})
    response.set_cookie("csrftoken", get_token(request))
    return response

def calculate_route(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user = request.user
            account_type = "Admin" if user.is_superuser else "Standard user"
            data = {
                'account_type': account_type,
                'countries': Airport.objects.all().order_by('country').values_list('country', flat=True).distinct(),
                'cities': Airport.objects.all().order_by('city').exclude(city='').values_list('city', flat=True).distinct(),
                'airports': Airport.objects.all().order_by('name').values_list('name', flat=True).distinct(),
                'planes': Plane.objects.all().order_by('name').values_list('name', flat=True).distinct(),
            }
            response = render(request, 'calculate_route.html', {'data': data})
        elif request.method == 'POST':
            json_data = json.loads(request.body)
            flight = Flight()
            flight.plane = Plane.objects.get(name=json_data['plane'])
            flight.departure_airport = Airport.objects.get(name=json_data['dep_airport'])
            flight.arrival_airport = Airport.objects.get(name=json_data['arr_airport'])
            flight.alternate_airport = Airport.objects.get(name=json_data['alt_airport'])
            flight.departure_time = datetime.strptime(json_data['dep_time'], '%Y-%m-%dT%H:%M:%S')
            result = flight.calculate_route()
            if result['result'] == 'Success':
                flight.calculate_arrival_time()
                result['arrival_time']=str(flight.arrival_time)
            result = json.dumps(result)
            print(result)
            response = JsonResponse(result, content_type='application/json', safe=False, status=200)
        else:
            result = {
                'result': 'Incorrect type of request'
            }
            response = render(request, 'result_unauth.html', {'result': result})
    else:
        result = {
            'result': 'You are not authenticated!',
        }
        response = render(request, 'result_unauth.html', {'result': result})
    response.set_cookie("csrftoken", get_token(request))
    return response

def responsive_form_data(request):
    if request.method == 'GET':
        airports = Airport.objects.all()
        cities = ''
        if request.GET.__contains__('country'):
            airports = airports.filter(country=request.GET.__getitem__('country')).order_by('name').values_list('name', flat=True).distinct()
            cities = airports.order_by('city').exclude(city='').values_list('city', flat=True).distinct()
            data = {
                'cities': list(cities),
                'airports': list(airports),
            }
            data = json.dumps(data)
        elif request.GET.__contains__('city'):
            countries = airports.filter(city=request.GET.__getitem__('city')).values_list('country', flat=True).distinct()

            data = [
                {
                    'country': c,
                    'airports': list(airports.filter(city=request.GET.__getitem__('city'), country=c).order_by('name').values_list('name', flat=True).distinct()),
                } for c in countries
            ]
            print(data)
            data = json.dumps(data)
        elif request.GET.__contains__('airport'):
            airport = airports.get(name=request.GET.__getitem__('airport'))
            data = {
                'country': airport.country,
                'city': airport.city,
            }
        else:
            data = {
                'result': 'Incorrect request parameters'
            }
            data = json.dumps(data)
        response = JsonResponse(data, content_type='application/json', safe=False, status=200)
    else:
        result = {
            'result': 'Incorrect type of request'
        }
        response = render(request, 'result_unauth.html', {'result': result})
    return response