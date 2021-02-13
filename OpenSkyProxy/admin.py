from django.contrib import admin
from .models import Plane, Airport, Flight, Waypoint

admin.site.register(Plane)
admin.site.register(Airport)
admin.site.register(Flight)
admin.site.register(Waypoint)