from opensky_api import OpenSkyApi
from collections import OrderedDict
from datetime import datetime
from .models import Flight
from django.contrib.gis.geos import Polygon

def get_flight_radar_data(bounds):
    now = datetime.now()
    flights = Flight.objects.filter(departure_time__lt=now, arrival_time__gt=now)

    for f in flights:
        f.calculate_location() # bounds = [lamin, lamax, lomin, lomax]


    # poly = Polygon(((bounds[0], bounds[2]), (bounds[0], bounds[3]), (bounds[1], bounds[3]), (bounds[1], bounds[2]), (bounds[0], bounds[2])))
    #
    # for f in flights:
    #     print(poly.contains(f.location))
    # flights = Flight.objects.filter(location__within=poly)
    # #departure_time__lt=now, arrival_time__gt=now,

    to_be_deleted = []
    for f in flights:
        print("min_lat: " + str(bounds[0]) + 'real_lat: ' + str(f.location.x) + "max_lat: " + str(bounds[1]))
        print("min_lng: " + str(bounds[2]) + 'real_lng: ' + str(f.location.y) + "max_lng: " + str(bounds[3]))
        if f.location.x<bounds[0] or f.location.x>bounds[1] or f.location.y<bounds[2] or f.location.y>bounds[3]:
            to_be_deleted.append(f.id)
    # print(to_be_deleted)
    flights.exclude(pk__in=to_be_deleted)

    api = OpenSkyApi()
    states = api.get_states(bbox=bounds)#[48.943315, 55.060033, 13.549301, 24.686826])

    geojson = to_geojson(states, flights)
    return geojson

def to_geojson(open_sky_data, local_data):
    f = [
        OrderedDict(
            type='Feature',
            id=ac.icao24,
            geometry=OrderedDict(type='Point', coordinates=[ac.longitude, ac.latitude]),
            properties=[]#OrderedDict(zip(keys, ac))
        ) for ac in open_sky_data.states
    ]

    lf = [
        OrderedDict(
            type='Feature',
            id=f.id,
            geometry=OrderedDict(type='Point', coordinates=[f.location.x, f.location.y])
        ) for f in local_data
    ]
    #print(lf)
    return dict(
        type='FeatureCollection',
        features=f + lf
    )