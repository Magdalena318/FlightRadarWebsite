from django import forms
from .models import Plane, Airport


class AddFlightForm(forms.Form):
    airports = Airport.objects.all().order_by('name').distinct('name')
    planes = Plane.objects.all().order_by('name').distinct('name')

    airports_choices = []
    for a in airports:
        airports_choices.append((a.id, a.name))

    planes_choices = []
    for p in planes:
        planes_choices.append((p.name, p.name))

    departure_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'input', 'type':'datetime-local'}))
    departure_airport = forms.ChoiceField(choices=airports_choices, widget=forms.Select(attrs={'class':'input'}))
    arrival_time = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':'input', 'type':'datetime-local'}))
    arrival_airport = forms.ChoiceField(choices=airports_choices, widget=forms.Select(attrs={'class':'input'}))
    alternate_airport = forms.ChoiceField(choices=airports_choices, widget=forms.Select(attrs={'class':'input'}))
    plane = forms.ChoiceField(choices=planes_choices, widget=forms.Select(attrs={'class':'input'}))

