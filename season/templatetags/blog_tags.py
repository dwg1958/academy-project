
## TAGS ########################################
from django import template
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ..models import TeamProfile, ScoringEvent, Parameter, User
from account.models import Profile
from django.utils import timezone
from datetime import datetime, timedelta, time
import time

# Set text fields to use Markdown #
from django.utils.safestring import mark_safe
import markdown


register = template.Library()
#################################################
## SIMPLE TAG ###################################
#################################################

# Count Number of teams #################
@register.simple_tag(name='teamCountTag')
def total_teams():
    return TeamProfile.objects.count()


# Return Team Update Blocked Message ############
@register.simple_tag(name='TeamUpdatesOK')
def team_update_on():
    # Get parameter for update banned
    para = Parameter.objects.get(name="update_team_allowed")

    #See whether there are any live events unscored
    now = timezone.now()
    next_event = ScoringEvent.objects.filter(results_in = False).order_by('startDateTime')[:1]

    # If there are, update the parameter
    for event in next_event:
        if event.startDateTime < now:
            #print('\n Overdue event: ',event.startDateTime, ' ', event.event_ID,  '\n')
            para.value = 0
            para.text = ">>> Team Updates Paused for " + str(event.event_ID) + " <<<"
            para.save()
            
    return para.text

#################################################
## INCLUSION TAG ################################
#################################################

# Plain Text event calendar
@register.inclusion_tag('season/tag_player_card.html', takes_context=True)
def tag_player_card(context):
    user = context['request'].user  # you have to pass the environment vars into this codeblock #
    myTeam    = TeamProfile.objects.get(pk=user.team.id)
    myProfile = Profile.objects.get(pk=user.id)
    league_total_teams = Parameter.objects.get(name="league_total_teams")
    return {'user': user, 'myProfile': myProfile, 'myTeam': myTeam , 'league_total_teams': league_total_teams}


# Sidebar event calendar ################
@register.inclusion_tag('season/tag_next_race_sidebar.html')
def tag_show_next_race_sidebar(count=10):
    next_races = ScoringEvent.objects.filter(results_in="False").order_by('startDateTime')[:count]
    return {'next_races': next_races}


# Sidebar event calendar ################
@register.inclusion_tag('season/tag_pi_formula_points.html', takes_context=True)
def tag_pi_formula_points(context):
    user = context['request'].user
    myteam = TeamProfile.objects.get(pk=user.team.id)
    return {'scores':[myteam.points_f1, myteam.points_f2, myteam.points_f3, myteam.points_ws, ]}






#################################################
## FILTERS ######################################
#################################################
@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))


@register.filter(name='daysuntil')
def daysuntil(date):
    delta = datetime.date(date) - datetime.now().date()
    return delta.days
