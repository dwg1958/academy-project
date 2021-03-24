
## TAGS ########################################
from django import template
from ..models import TeamProfile, ScoringEvent
from datetime import datetime


register = template.Library()

## SIMPLE TAG ##################################
@register.simple_tag(name='teamCountTag')
def total_teams():
    return TeamProfile.objects.count()


## INCLUSION TAG ################################
# Plain Text event calendar
@register.inclusion_tag('season/next_race.html')
def show_next_race(count=5):
    next_races = ScoringEvent.objects.all().order_by('startDateTime')[:count]
    for race in next_races:
        race.name = race.name#.ljust(30, ' ')
    return {'next_races': next_races}


# Sidebar event calendar ################
@register.inclusion_tag('season/next_race_sidebar.html')
def show_next_race_sidebar(count=10):
    next_races = ScoringEvent.objects.filter(results_in="False").order_by('startDateTime')[:count]
    return {'next_races': next_races}


## FILTERS ######################################

# Set text fields to use Markdown #
from django.utils.safestring import mark_safe
import markdown

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.filter(name='daysuntil')
def daysuntil(date):
    delta = datetime.date(date) - datetime.now().date()
    return delta.days
