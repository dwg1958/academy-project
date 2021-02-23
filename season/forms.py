
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
'''
class EditTeamProfileF1Form(forms.ModelForm):
    class Meta:
        model = TeamProfile
        fields = ('teamName','p1_1', 'p1_2', 'p1_m')

    def __init__(self, *args, submission=None):
        super().__init__(*args)
        self.submission = submission
        self.fields['p1_1'].choices = Competitor.objects.filter(formula='1', role='D').values_list('id', 'surname')
        self.fields['p1_2'].choices = Competitor.objects.filter(formula='1', role='D').values_list('id', 'surname')
        self.fields['p1_m'].choices = Competitor.objects.filter(formula='1', role='M').values_list('id', 'surname')
'''
