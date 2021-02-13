from .models import Airports
from django.contrib.gis.geos import Point

data = open('airports.dat', 'r')

for line in data:
    parts = line.split(',')
    airport = Airports()
    airport.name = parts[1]
    airport.city = parts[2]
    airport.country = parts[3]
    airport.id = parts[4]
    airport.location = Point(parts[6], parts[7])
    airport.save()

from OpenSkyProxy.models import connect_waypoints
from OpenSkyProxy.models import Waypoint
from OpenSkyProxy.models import waypoint_population
Waypoint.connect_waypoints(Waypoint)
connect_waypoints()


from OpenSkyProxy.models import waypoints_to_airports
from OpenSkyProxy.models import Waypoint, Airport
waypoints_to_airports()