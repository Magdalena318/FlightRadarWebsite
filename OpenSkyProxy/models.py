import uuid
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point, LineString
import xml.etree.ElementTree as ET
from math import sin, cos, sqrt, atan2, radians
import json
from django.core.serializers import serialize
from datetime import timedelta
from datetime import datetime
import math

class Waypoint(models.Model):
    name = models.CharField(max_length=50, primary_key=True, unique=True, default=uuid.uuid4)
    location = models.PointField(null=True)
    adj = models.ManyToManyField("self", blank=True)

    objects = models.Manager()

    def from_xml(self, el):
        if Waypoint.objects.filter(name = el.find('name').text).exists():
            return
        else:
            self.name = el.find('name').text
            print(self.name)
            self.location = Point(float(el.attrib['lat']), float(el.attrib['lon']))
            self.save()

    def from_airports(self):
        airports = Airport.objects.all()
        for a in airports:
            w = Waypoint()
            w.name = a.name
            w.location = a.location

class Airport(models.Model):
    id = models.CharField(max_length=50, primary_key=True, unique=True, default=uuid.uuid4) #IATA code
    name = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=50, null=True)
    location = models.PointField(null=True)

    adj = models.ManyToManyField(Waypoint, blank=True)

    objects = models.Manager()

    def from_file(self, line):
        tmp = line.replace('\n', '')
        parts = tmp.split(';')
        self.name = parts[0].strip()
        self.city = parts[1].strip()
        self.country = parts[2].strip()
        self.id = parts[3].strip()
        self.location = Point(float(parts[4]), float(parts[5]))
        self.save()

    def from_json(self, json):
        self.name = json['name']
        self.city = json['city']
        self.country = json['country']
        self.id = json['id']
        self.location = Point(json['lat'], json['lng'])
        self.save()

class Plane(models.Model):
    name = models.CharField(max_length=50, primary_key=True, unique=True, default=uuid.uuid4)
    flight_range = models.FloatField(null=True)
    speed = models.FloatField(null=True)
    max_passenger = models.IntegerField(null=True)

    objects = models.Manager()

    def from_file(self, line):
        tmp = line.replace('\n', '')
        #print(line)
        parts = tmp.split(';')
        self.name = parts[0].strip()
        if 'Adamjet' in self.name:
            print(self.name)
        self.flight_range = float(parts[1].replace(' ', ''))
        self.speed = float(parts[2].replace(' ', ''))
        self.max_passenger = int(parts[3].replace(' ', ''))
        self.save()

    def from_json(self, json):
        self.name = json['name']
        self.flight_range = json['flight_range']
        self.speed = json['speed']
        self.max_passenger = json['max_passenger']
        self.save()

#Distance in km for two latlng Points
def haversine(p1, p2):
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(p1.x)
    lon1 = radians(p1.y)
    lat2 = radians(p2.x)
    lon2 = radians(p2.y)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

#Find a point on a line at a given distance
def cut(line, distance):
    if distance <= 0.0 or distance >= line.length:
        return line.coords[1]
    elif line.length < distance*2:
        return line.interpolate(line.length/2)
    else:
        return line.interpolate(distance)

class Flight(models.Model):
    id = models.CharField(max_length=50, primary_key=True, unique=True, default=uuid.uuid4)
    location = models.PointField(null=True)

    departure_time = models.DateTimeField(null=True)
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='%(class)s_departure_airport', null=True)

    arrival_time = models.DateTimeField(null=True)
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='%(class)s_arrival_airport', null=True)
    alternate_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='%(class)s_alternate_airport', null=True)

    plane = models.ForeignKey(Plane, on_delete=models.CASCADE, related_name='%(class)s_plane', null=True)
    route = models.LineStringField(null=True)

    objects = models.Manager()

    def calculate_route(self):
        #FLight range check
        base_distance = haversine(self.departure_airport.location, self.arrival_airport.location)
        alt_distance = base_distance + haversine(self.arrival_airport.location, self.alternate_airport.location)
        if base_distance * 1.1 > self.plane.flight_range:
            return {'result': 'Failure', 'reason': 'Distance between the origin and destination is bigger than the flight range!'}
        if alt_distance * 1.1 > self.plane.flight_range:
            return {'result': 'Failure', 'reason': 'Distance in case of alternative destination landing is bigger than the flight range!'}

        min_cut_distance = 5
        max_cut_distance = 10
        local_route = []
        local_route.append(self.departure_airport.location)
        waypoint_route = []
        waypoint_route.append(self.departure_airport.name)

        #Check if the route needs to be cut
        if self.departure_airport.location.distance(self.arrival_airport.location)<=max_cut_distance:
            self.route = LineString(self.departure_airport.location, self.arrival_airport.location)
            local_route.append(self.arrival_airport.location)
            list_json = [(p.x, p.y) for p in local_route]
            waypoint_route.append(self.arrival_airport.name)
            return {'result': 'Success', 'reason': 'Flight has been submitted successfully!', 'route': list_json, 'waypoints': waypoint_route}

        #Add first cut to the route
        straight_route_line = LineString(self.departure_airport.location, self.arrival_airport.location)
        next_cut = cut(straight_route_line, (max_cut_distance+min_cut_distance)/2)
        next_stop = Waypoint()
        min_distance = 100000000
        for w in self.departure_airport.adj.all():
            distance = w.location.distance(next_cut)
            if distance < min_distance:
                next_stop = w
                min_distance = distance
        local_route.append(next_stop.location)
        waypoint_route.append(next_stop.name)

        while next_stop!=self.arrival_airport:
            min_distance = 100000000
            straight_route_line = LineString(next_stop.location, self.arrival_airport.location)
            next_cut = cut(straight_route_line, (max_cut_distance + min_cut_distance) / 2)
            if next_cut == self.arrival_airport.location or next_stop.location.distance(self.arrival_airport.location)<=max_cut_distance:
                next_stop=self.arrival_airport
                local_route.append(next_stop.location)
                waypoint_route.append(next_stop.name)
            else:
                for w in next_stop.adj.all():
                    distance = w.location.distance(next_cut)
                    if distance < min_distance:
                        next_stop = w
                        min_distance = distance
                local_route.append(next_stop.location)
                waypoint_route.append(next_stop.name)
        self.route = LineString([(pt.x, pt.y) for pt in local_route])
        list_json = [(p.x, p.y) for p in local_route]
        result = {'result': 'Success', 'reason': 'Flight has been submitted successfully!', 'route': list_json, 'waypoints': waypoint_route}
        return result

    def calculate_arrival_time(self):
        distance = 0
        prev = None
        for w in self.route:
            if not prev:
                prev = w
            else:
                distance += haversine(Point(prev), Point(w))
                prev = w
        speed = self.plane.speed
        time = distance / speed # in hours
        num_hours = math.floor(time)
        num_minutes = math.floor((time-num_hours)*60)
        if isinstance(self.departure_time, str):
            departure_time = datetime.strptime(self.departure_time, '%Y-%m-%dT%H:%M:%S')
        else:
            departure_time = self.departure_time
        self.arrival_time = departure_time+timedelta(hours=num_hours, minutes=num_minutes)

    def calculate_location(self):
        if isinstance(self.departure_time, str):
            departure_time = datetime.strptime(self.departure_time, '%Y-%m-%dT%H:%M:%S')
        else:
            departure_time = self.departure_time

        if self.arrival_time<datetime.now():
            self.location = self.arrival_airport.location

        if self.departure_time > datetime.now():
            self.location = self.departure_airport.location
        else:
            cur_time = datetime.now() - departure_time
            cur_time = cur_time.total_seconds() / (60 * 60)

        cur_distance=self.plane.speed*cur_time

        prev = None
        for w in self.route:
            if not prev:
                prev = w
            else:
                if cur_distance-haversine(Point(prev), Point(w))>0:
                    cur_distance -= haversine(Point(prev), Point(w))
                    prev = w
                else:
                    straight_route_line = LineString(Point(prev), Point(w))
                    next_cut = cut(straight_route_line, cur_distance)
                    print(next_cut)
                    if isinstance(next, Point):
                        self.location = next_cut
                    else:
                        self.location = Point(next_cut)
                    break

#helper functions for loading the data
def airport_population():
    Airport.objects.all().delete()
    # Loading Airport database from file
    airport_path = 'E:\Projects\FlightRadar\Back-end\FlightRadar\OpenSkyProxy\Data\\airports.txt'
    airport_data = open(airport_path, 'r', encoding='mbcs')
    count = 0
    for line in airport_data:
        entry = Airport()
        entry.from_file(line)
        entry.save()
        count += 1

def waypoint_population():
    Waypoint.objects.all().delete()
    waypoint_path = 'E:\Projects\FlightRadar\Back-end\FlightRadar\OpenSkyProxy\Data\waypoints.xml'
    root = ET.parse(waypoint_path).getroot()
    for el in root.findall('wpt'):
         w = Waypoint()
         w.from_xml(el)

def plane_population():
    Plane.objects.all().delete()
    # Loading Airport database from file
    planes_path = 'E:\Projects\FlightRadar\Back-end\FlightRadar\OpenSkyProxy\Data\\airplanes.txt'
    planes_data = open(planes_path, 'r', encoding='mbcs')
    for line in planes_data:
        entry = Plane()
        entry.from_file(line)

def connect_waypoints():
    for w in Waypoint.objects.all():
        w.adj.clear()

    set1 = Waypoint.objects.all()
    set2 = Waypoint.objects.all()
    count = 0
    for w1 in set1:
        for w2 in set2:
            if w1!=w2:# or w1.adj.filter(pk=w2.name).exists():
                distance = w1.location.distance(w2.location)
                if distance>=5 and distance<=10:
                    w1.adj.add(w2)
                    w2.adj.add(w1)
                    print('Added')
        count += 1
        print(count)
        set2.exclude(pk=w1.name)

def waypoints_to_airports():
    for w in Airport.objects.all():
        w.adj.clear()

    count = 0
    for w1 in Airport.objects.all():
        for w2 in Waypoint.objects.all():
            distance = w1.location.distance(w2.location)
            if distance>=5 and distance<=10:
                w1.adj.add(w2)
                print('Added')
        count += 1
        print("Airport number: " + str(count))