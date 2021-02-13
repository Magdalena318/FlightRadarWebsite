from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('planes_data/', views.planes_data, name="planesdata"),
    path('lookup/', views.lookup, name="lookup"),
    path('lookup-airplanes/', views.lookup_planes, name="planeslookup"),
    path('lookup-airports/', views.lookup_airports, name="airportslookup"),
    path('lookup-flights/', views.lookup_flights, name="flightslookup"),
    path('add/', views.add_flight, name="addflight"),
    path('route/', views.calculate_route, name="calculateroute"),
    path('responsive-form/', views.responsive_form_data, name="responsiveformdata"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
