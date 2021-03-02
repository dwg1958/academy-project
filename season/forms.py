
from django import forms
from .models import Event, TeamProfile, Competitor

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'date', 'circuit', 'country', 'formulas', 'startDateTime', 'endDateTime')
        date          = forms.DateTimeField(input_formats=['%d/%m/%Y'])
        startDateTime = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])
        endDateTime   = forms.DateTimeField(input_formats=['%d/%m/%Y %H:%M'])

class TeamProfileForm(forms.ModelForm):
    class Meta:
        model = TeamProfile
        fields = ('teamName', 'teamLogo')
