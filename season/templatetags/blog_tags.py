
## TAGS ########################################
from django import template
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ..models import TeamProfile, ScoringEvent, Parameter, User, Event
from account.models import Profile
from django.utils import timezone
from datetime import datetime, timedelta, time
from django.db.models import F
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
    user               = context['request'].user  # you have to pass the environment vars into this codeblock #
    myTeam             = TeamProfile.objects.get(pk=user.team.id)
    myProfile          = Profile.objects.get(pk=user.id)
    league_total_teams = Parameter.objects.get(name="league_total_teams")
    position           = user.team.league_position
    percentile         = position / len(TeamProfile.objects.all()) * 100
    print(percentile)


    return {'user': user, 'myProfile': myProfile, 'myTeam': myTeam , 'league_total_teams': league_total_teams, 'percentile':percentile}


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

# Hall of Fame ################
@register.inclusion_tag('season/tag_hall_of_fame.html', takes_context=True)
def tag_hall_of_fame(context):
    league_list  = TeamProfile.objects.all().order_by('-points_total')[:5]
    return {'league_list':league_list}

# Hall of Fame ################
@register.inclusion_tag('season/tag_events_so_far.html', takes_context=True)
def tag_events_so_far(context):

    progress_list=[]
    progress_list.append( Parameter.objects.get(name="events_in_1").value )
    progress_list.append( Parameter.objects.get(name="events_total_1").value )
    progress_list.append( Parameter.objects.get(name="events_in_2").value )
    progress_list.append( Parameter.objects.get(name="events_total_2").value )
    progress_list.append( Parameter.objects.get(name="events_in_3").value )
    progress_list.append( Parameter.objects.get(name="events_total_3").value )
    progress_list.append( Parameter.objects.get(name="events_in_W").value )
    progress_list.append( Parameter.objects.get(name="events_total_W").value )
    progress_list.append( Parameter.objects.get(name="events_in_ALL").value )
    progress_list.append( Parameter.objects.get(name="events_total_ALL").value )

    data = []
    data.append(progress_list[0]/progress_list[1]*100)
    data.append(progress_list[2]/progress_list[3]*100)
    data.append(progress_list[4]/progress_list[5]*100)
    data.append(progress_list[6]/progress_list[7]*100)

    next = []
    date = []

    next_race_1 = Event.objects.filter(startDateTime__gt = timezone.now()).filter(formulas__contains='1')[:1][0]
    next.append(next_race_1.name)
    date.append(next_race_1.startDateTime)
    next_race_2 = Event.objects.filter(startDateTime__gt = timezone.now()).filter(formulas__contains='2')[:1][0]
    next.append(next_race_2.name)
    date.append(next_race_2.startDateTime)
    next_race_3 = Event.objects.filter(startDateTime__gt = timezone.now()).filter(formulas__contains='3')[:1][0]
    next.append(next_race_3.name)
    date.append(next_race_3.startDateTime)
    next_race_w = Event.objects.filter(startDateTime__gt = timezone.now()).filter(formulas__contains='W')[:1][0]
    next.append(next_race_w.name)
    date.append(next_race_w.startDateTime)




    return { 'progress_list':progress_list, 'data':data, 'next':next, 'date':date }



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
