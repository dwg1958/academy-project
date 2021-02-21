from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Competitor, Event, ScoringEvent, Result
from django.contrib.auth.decorators import login_required
from .forms import EventForm, TeamProfileForm

# Create your views here.

############################### GUEST PAGES ###################################################

## Show Events
def showevents(request):
    # Fill lower table with all extant data
    allevents = Event.objects.all()
    return render(request, 'season/showevents.html',{'allevents':allevents})

def showscoringevents(request):
    allevents = ScoringEvent.objects.all()
    return render(request, 'season/showscoringevents.html', {'allevents': allevents})

def showresults(request):
    resultset = Result.objects.order_by('scoringEvent_ID', 'finishPosition')

    return render(request, 'season/showresults.html', {'resultset': resultset})

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

    #pers_data = get_object_or_404(Competitor,pk=11)
    #pers_data = get_list_or_404(Competitor,pk=per)

    #"pers_data": pers_data,

    return render(request, 'season/tables.html', {'personality':pers_data, 'competitors': competitors,'managers':managers,'formulaname':formulaname, 'formula':formula, 'showPersonal':showPersonal})




############################### USER PAGES ###################################################

@login_required
##### SHOW MY TEAM ###################
def teamview(request):
    return render(request, 'season/teamview.html') #, {'competitors': competitors})



@login_required
### EDIT MY TEAM #@@@@@@@@@#########
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
