
## TAGS ########################################
from django import template
from ..models import TeamProfile, ScoringEvent

register = template.Library()

## SIMPLE TAG ##################################
@register.simple_tag(name='teamCountTag')

def total_teams():
    return TeamProfile.objects.count()


## INCLUSION TAG ################################
@register.inclusion_tag('season/next_race.html')
def show_next_race(count=5):
    next_races = ScoringEvent.objects.all().order_by('startDateTime')[:count]
    for race in next_races:
        race.name = race.name.ljust(30, ' ')
    return {'next_races': next_races}


## FILTERS ######################################
from django.utils.safestring import mark_safe
import markdown

@register.filter(name='markdown')

def markdown_format(text):
    return mark_safe(markdown.markdown(text))
