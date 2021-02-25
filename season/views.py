from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Competitor, Event, ScoringEvent, Result, TeamProfile
from django.contrib.auth.decorators import login_required
from .forms import EventForm, TeamProfileForm
from django.contrib.auth.models import User

# Create your views here.

############################### GUEST PAGES ###################################################

## Show Events ####################
def showevents(request):
    # Fill lower table with all extant data
    allevents = Event.objects.all()
    return render(request, 'season/showevents.html',{'allevents':allevents})

####################################
def showscoringevents(request):
    allevents = ScoringEvent.objects.all()
    return render(request, 'season/showscoringevents.html', {'allevents': allevents})

####################################
def showresults(request):
    resultset = Result.objects.order_by('scoringEvent_ID', 'finishPosition')

    return render(request, 'season/showresults.html', {'resultset': resultset})

####################################
def tables(request):
#	textreceived = request.GET['fname']
    competitors = Competitor.objects
    return render(request, 'season/tables.html', {'competitors': competitors})


#### SHOW COMPETITOR TABLES #######
def tableformula(request, formula):

    # Go find drivers in this formula only
    if formula == "4" or formula == "W":
        formula = "W"
        formulaname = "W Series"
    else:
        formulaname = "Formula " + formula

    competitors = Competitor.objects.filter(formula=formula, role="D")
    managers    = Competitor.objects.filter(formula=formula, role="M")

    ## Find personality dataset
    try:
        per = request.GET['per']
        pers_data = Competitor.objects.filter(surname=per)
        showPersonal = "show"
    except:
        pers_data = list(competitors[:1])
        showPersonal = " "

    return render(request, 'season/tables.html', {'personality':pers_data, 'competitors': competitors,'managers':managers,'formulaname':formulaname, 'formula':formula, 'showPersonal':showPersonal})

def test(request):
    #resultset = Result.objects.order_by('scoringEvent_ID', 'finishPosition')

    return render(request, 'season/test.html')#, {'resultset': resultset})


############################### USER PAGES ###################################################

@login_required
##### SHOW AND EDIT MY TEAM ###################
def teamview(request):

    if(request.method == "POST"):
        # Go find the record we want to update
        recordtoedit = TeamProfile.objects.get(pk=request.user.team.id) # still using our 1to1 field relation
        ## ToDo - SAVE OLD VERSION TO ARCHIVE ###

        # Now change relevant fields
        if 'F1_submit' in request.POST:
            print('F1 submit found')
            recordtoedit.p1_1 = Competitor.objects.get(pk=request.POST['p1_1'])
            recordtoedit.p1_2 = Competitor.objects.get(pk=request.POST['p1_2'])
            #Save data to table
            recordtoedit.save()
            returnURL = 'season/teamview.html?tab=F1'

        elif 'F2_submit' in request.POST:
            print('F2 submit found')
            print('p2_1 =',request.POST['p2_1'])
            print('p2_2 =',request.POST['p2_2'])
            recordtoedit.p2_1 = Competitor.objects.get(pk=request.POST['p2_1'])
            recordtoedit.p2_2 = Competitor.objects.get(pk=request.POST['p2_2'])
            #Save data to table
            recordtoedit.save()
            returnURL = 'season/teamview.html?tab=F2'

        elif 'F3_submit' in request.POST:
            print('F3 submit found')
            print('p3_1 =',request.POST['p3_1'])
            print('p3_2 =',request.POST['p3_2'])
            recordtoedit.p3_1 = Competitor.objects.get(pk=request.POST['p3_1'])
            recordtoedit.p3_2 = Competitor.objects.get(pk=request.POST['p3_2'])
            #Save data to table
            recordtoedit.save()
            returnURL = 'season/teamview.html?tab=F3'

        elif 'WS_submit' in request.POST:
            print('WS submit found')
            print('pw_1 =',request.POST['pw_1'])
            print('pw_2 =',request.POST['pw_2'])
            recordtoedit.pw_1 = Competitor.objects.get(pk=request.POST['pw_1'])
            recordtoedit.pw_2 = Competitor.objects.get(pk=request.POST['pw_2'])
            #Save data to table
            recordtoedit.save()
            returnURL = 'season/teamview.html?tab=WS'

    else:
        returnURL = 'season/teamview.html'

    #Now load (or reload) data to reshow form with new data in it.
    teamdata =  TeamProfile.objects.get(pk=request.user.team.id)
    f1drivers = Competitor.objects.filter(formula = 1, role = 'D')
    f2drivers = Competitor.objects.filter(formula = 2, role = 'D')
    f3drivers = Competitor.objects.filter(formula = 3, role = 'D')
    wsdrivers = Competitor.objects.filter(formula = 'W', role = 'D')
    return render(request, 'season/teamview.html',{ 'teamdata':teamdata, 'f1drivers':f1drivers, 'f2drivers':f2drivers, 'f3drivers':f3drivers, 'wsdrivers':wsdrivers})






@login_required
### EDIT MY TEAM #####################
def teampicker(request):
    return render(request, 'season/teampicker.html')

############################### ADMIN PAGES ###################################################

####################################
def addcompetitors(request):
    return render(request, 'season/add_competitors.html')


####### ADD/VIEW EVENTS ######
def addevents(request):
    new_event = None
    if request.method == 'POST':
        # A comment was posted
        event_form = EventForm(data=request.POST)
        if event_form.is_valid():
            # Create Event object but don't save to database yet
            new_event = event_form.save(commit=False)
            # Assign the current parent record to the data set
            # new_event.whatever = whatever  # Add extra data
            # Save the event to the database
            new_event.save()
            event_form = EventForm()
    else:
        event_form = EventForm()

    # Fill lower table with all extant data
    allevents = Event.objects.all()

    return render(request, 'season/add_events.html',{'new_event': new_event,'event_form': event_form, 'allevents':allevents})


####################################
def addscoringevents(request):
    return render(request, 'season/add_scoring_events.html')

####################################
def addresults(request):
    return render(request, 'season/add_results.html')
