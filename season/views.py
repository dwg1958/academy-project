from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .models import Competitor, Event, ScoringEvent, Result, TeamProfile, AcademyScoringMatrix, CompetitorScore
from django.contrib.auth.decorators import login_required
from .forms import EventForm, TeamProfileForm, TeamProfileForm
from django.contrib.auth.models import User
import time

# Create your views here.

############################### GUEST PAGES ###################################################

## Show Events ####################
def showevents(request):
    # Fill lower table with all extant data
    allevents = Event.objects.all()
    return render(request, 'season/showevents.html',{'allevents':allevents})


####################################
def showscoringevents(request):
    if request.method == 'GET' and 'event' in request.GET:
        event = request.GET['event']
        allevents = ScoringEvent.objects.filter(event_ID = event).order_by('startDateTime')
        eventname = Event.objects.get(id=event)
        return render(request, 'season/showscoringevents.html', {'eventname': eventname,'allevents': allevents})
    else:
        allevents = Event.objects.all()
        return render(request, 'season/showevents.html',{'allevents':allevents})


####################################
def showresults(request):
    if request.method == 'GET' and 'scoringevent' in request.GET:
        result_id = request.GET['scoringevent']
        resultset = Result.objects.filter(scoringEvent_ID=result_id).order_by('scoringEvent_ID', 'finishPosition')
        scoringeventname = ScoringEvent.objects.get(id=result_id)
        return render(request, 'season/showresults.html', {'resultset': resultset, 'scoringeventname':scoringeventname,'startDateTime':scoringeventname.startDateTime})
    else:
        allevents = Event.objects.all()
        return render(request, 'season/showevents.html',{'allevents':allevents})


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


####################################
def test(request):
    #resultset = Result.objects.order_by('scoringEvent_ID', 'finishPosition')

    return render(request, 'season/test.html')#, {'resultset': resultset})


############################### USER PAGES ###################################################

@login_required
##### SHOW AND EDIT MY TEAM ###################
def teamview(request):
    returnmessage = ""

    if(request.method == "POST"):
        # Go find the record we want to update
        recordtoedit = TeamProfile.objects.get(pk=request.user.team.id) # still using our 1to1 field relation

########## ToDo - SAVE OLD VERSION TO ARCHIVE ###

        # Now change relevant fields
        if 'F1_submit' in request.POST:
            # POST arg comes in as value="1|Lewis Hamilton|29.0"
            arg1 = request.POST['p1_1_picker'] #Get arg
            arg1 = arg1[:arg1.index("|")]      #Split out the first element - the driverID
            arg2 = request.POST['p1_2_picker']
            arg2 = arg2[:arg2.index("|")]

            new_p1_1 = Competitor.objects.get(pk=arg1) #Find new driver 1 record
            new_p1_2 = Competitor.objects.get(pk=arg2)
            #check budget not exceeded
            new_cash_pot = recordtoedit.f1_cashpot + recordtoedit.p1_1.value + recordtoedit.p1_2.value - new_p1_1.value - new_p1_2.value

            if ( new_cash_pot < 0 ):
                returnmessage = 'You have exceeded your budget - please choose again'
            elif ( arg1 == arg2 ):
                returnmessage = 'You have chosen the same driver twice - please choose again'
            else:
                recordtoedit.p1_1 = new_p1_1
                recordtoedit.p1_1_cost = new_p1_1.value
                recordtoedit.p1_2 = new_p1_2
                recordtoedit.p1_2_cost = new_p1_2.value
                recordtoedit.f1_cashpot = new_cash_pot
                #Save data to table
                recordtoedit.save()

            returnURL = 'season/teamview.html?tab=F1'

        elif 'F2_submit' in request.POST:
            # POST arg comes in as value="1|Lewis Hamilton|29.0"
            arg1 = request.POST['p2_1_picker'] #Get arg
            arg1 = arg1[:arg1.index("|")]      #Split out the first element - the driverID
            arg2 = request.POST['p2_2_picker']
            arg2 = arg2[:arg2.index("|")]

            new_p2_1 = Competitor.objects.get(pk=arg1) #Find new driver 2 record
            new_p2_2 = Competitor.objects.get(pk=arg2)
            #check budget not exceeded
            new_cash_pot = recordtoedit.f2_cashpot + recordtoedit.p2_1.value + recordtoedit.p2_2.value - new_p2_1.value - new_p2_2.value

            if ( new_cash_pot < 0 ):
                returnmessage = 'You have exceeded your budget - please choose again'
            elif ( arg1 == arg2 ):
                returnmessage = 'You have chosen the same driver twice - please choose again'
            else:
                recordtoedit.p2_1 = new_p2_1
                recordtoedit.p2_1_cost = new_p2_1.value
                recordtoedit.p2_2 = new_p2_2
                recordtoedit.p2_2_cost = new_p2_2.value
                recordtoedit.f2_cashpot = new_cash_pot
                #Save data to table
                recordtoedit.save()

            returnURL = 'season/teamview.html?tab=F2'

        elif 'F3_submit' in request.POST:
            arg1 = request.POST['p3_1_picker'] #Get arg
            arg1 = arg1[:arg1.index("|")]      #Split out the first element - the driverID
            arg2 = request.POST['p3_2_picker']
            arg2 = arg2[:arg2.index("|")]

            new_p3_1 = Competitor.objects.get(pk=arg1) #Find new driver 2 record
            new_p3_2 = Competitor.objects.get(pk=arg2)
            #check budget not exceeded
            new_cash_pot = recordtoedit.f3_cashpot + recordtoedit.p3_1.value + recordtoedit.p3_2.value - new_p3_1.value - new_p3_2.value

            if ( new_cash_pot < 0 ):
                returnmessage = 'You have exceeded your budget - please choose again'
            elif ( arg1 == arg2 ):
                returnmessage = 'You have chosen the same driver twice - please choose again'
            else:
                recordtoedit.p3_1 = new_p3_1
                recordtoedit.p3_1_cost = new_p3_1.value
                recordtoedit.p3_2 = new_p3_2
                recordtoedit.p3_2_cost = new_p3_2.value
                recordtoedit.f3_cashpot = new_cash_pot
                #Save data to table
                recordtoedit.save()

            returnURL = 'season/teamview.html?tab=F3'

        elif 'WS_submit' in request.POST:
            arg1 = request.POST['pw_1_picker'] #Get arg
            arg1 = arg1[:arg1.index("|")]      #Split out the first element - the driverID
            arg2 = request.POST['pw_2_picker']
            arg2 = arg2[:arg2.index("|")]

            new_pw_1 = Competitor.objects.get(pk=arg1) #Find new driver 2 record
            new_pw_2 = Competitor.objects.get(pk=arg2)
            #check budget not exceeded
            new_cash_pot = recordtoedit.ws_cashpot + recordtoedit.pw_1.value + recordtoedit.pw_2.value - new_pw_1.value - new_pw_2.value

            if ( new_cash_pot < 0 ):
                returnmessage = 'You have exceeded your budget - please choose again'
            elif ( arg1 == arg2 ):
                returnmessage = 'You have chosen the same driver twice - please choose again'
            else:
                recordtoedit.pw_1 = new_pw_1
                recordtoedit.pw_1_cost = new_pw_1.value
                recordtoedit.pw_2 = new_pw_2
                recordtoedit.pw_2_cost = new_pw_2.value
                recordtoedit.ws_cashpot = new_cash_pot
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
    return render(request, 'season/teamview.html',{ 'returnmessage':returnmessage, 'teamdata':teamdata, 'f1drivers':f1drivers, 'f2drivers':f2drivers, 'f3drivers':f3drivers, 'wsdrivers':wsdrivers})


@login_required
### EDIT MY TEAM #####################
def teamnamepicker(request):
    if request.method == 'POST':
        team_form = TeamProfileForm(
                                    instance=request.user.team,
                                    data=request.POST,
                                    files=request.FILES)
        if team_form.is_valid():
            team_form.save()
            return redirect('teamnamepicker')
    else:
        team_form = TeamProfileForm(instance=request.user.team)
    return render(request,'season/teamnamepicker.html', {'team_form': team_form})

############################### ADMIN PAGES ###################################################
@login_required
####################################
def addcompetitors(request):
    return render(request, 'season/add_competitors.html')


@login_required
####### ADD/VIEW EVENTS #######################################################################
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


@login_required
##############################################################################################
def scoreevents(request):
    #1. Select event to score
    if "scoringevent" in request.GET:

        #Start Timer
        tic = time.perf_counter()

        #Get Scoring Event details
        scoringevent_ID = int(request.GET['scoringevent'])
        scoringevent_detail = ScoringEvent.objects.get(pk=scoringevent_ID)
        EventName = scoringevent_detail.name + ' (Type:' + scoringevent_detail.eventType + ')'

        # Get Scoring Matrix #############
        matrix = AcademyScoringMatrix.objects.all()
        ASM_1 = matrix.get(formula=scoringevent_detail.formula, teamPosition='1')
        ASM_2 = matrix.get(formula=scoringevent_detail.formula, teamPosition='2')
        resultsArray = []

        #Set Event type
        if   scoringevent_detail.eventType in 'RF3':    rt = 'm_'
        elif scoringevent_detail.eventType in '12S':    rt = 's_'
        else:                                           rt = 'q_'

        #2. For each result
        resultset = Result.objects.filter(scoringEvent_ID=int(scoringevent_ID)).order_by('finishPosition')

        #Make array for new records to batch upload at the endDateTimecompetitorScores = []
        competitorScores = []

        # 2.1 select relevant scoring matrix records (e.g. F1_D1 *AND* F2_D2) then go
        # through each scoring opportunity and make a competitor_score record with EACH score for EACH TeamPosition
        for result in resultset:

            #Give Points for P1 thru P10
            var = rt+str(result.finishPosition)
            if result.finishPosition < 11:
                t1_pos_points = getattr(ASM_1,var)
                t2_pos_points = getattr(ASM_2,var)

                # Make new competitor score record
                competitorScore = CompetitorScore()
                competitorScore.result_ID  = result
                competitorScore.pointsType = 'P'
                competitorScore.t1_score   = t1_pos_points
                competitorScore.t2_score   = t2_pos_points
                competitorScores.append(competitorScore)

            else:
                t1_pos_points = t2_pos_points = 0

            # Disqualified Points
            var = rt + 'disqualified'
            if result.disqualified:
                t1_disqualified = 0-getattr(ASM_1,var)
                t2_disqualified = 0-getattr(ASM_2,var)
                # Make new competitor score record
                competitorScore = CompetitorScore()
                competitorScore.result_ID  = result
                competitorScore.pointsType = 'D'
                competitorScore.t1_score   = t1_disqualified
                competitorScore.t2_score   = t2_disqualified
                competitorScores.append(competitorScore)
            else:
                t1_disqualified = t2_disqualified = 0

            # On Quali events, put in blank N/A values for FLap, placesGainedLost, lapsBehind
            t1_fLap  = placesGainedLost = laps_off_leader = t1_PlacesGainedLost = t1_lapsLost =t2_fLap  = t2_PlacesGainedLost = t1_lapsLost = t2_lapsLost = 0

            #Now get Points for other scoring actions for races only
            if rt != 'q_':
                # Fastest Lap Points
                var = rt + 'fastest_lap'
                if result.fastestLap:
                    t1_fLap = getattr(ASM_1,var)
                    t2_fLap = getattr(ASM_2,var)
                    # Make new competitor score record
                    competitorScore = CompetitorScore()
                    competitorScore.result_ID  = result
                    competitorScore.pointsType = 'F'
                    competitorScore.t1_score   = t1_fLap
                    competitorScore.t2_score   = t2_fLap
                    competitorScores.append(competitorScore)
                else:
                    t1_fLap = t2_fLap = 0


                # Places gained/lost points
                placesGainedLost = result.finishPosition - result.startPosition
                if placesGainedLost != 0:
                    var = rt + 'pos_gained'
                    t1_PlacesGainedLost = placesGainedLost * getattr(ASM_1,var)
                    t2_PlacesGainedLost = placesGainedLost * getattr(ASM_2,var)
                    # Make new competitor score record
                    competitorScore = CompetitorScore()
                    competitorScore.result_ID  = result
                    competitorScore.pointsType = 'G'
                    competitorScore.t1_score   = t1_PlacesGainedLost
                    competitorScore.t2_score   = t2_PlacesGainedLost
                    competitorScores.append(competitorScore)
                else:
                    t1_PlacesGainedLost =0
                    t2_PlacesGainedLost =0

                # Laps behind leader points
                laps_off_leader = result.laps_off_leader
                if laps_off_leader > 0:
                    var = rt + 'laps_off_leader'
                    t1_lapsLost = 0-laps_off_leader * getattr(ASM_1,var)
                    t2_lapsLost = 0-laps_off_leader * getattr(ASM_2,var)
                    # Make new competitor score record
                    competitorScore = CompetitorScore()
                    competitorScore.result_ID  = result
                    competitorScore.pointsType = 'L'
                    competitorScore.t1_score   = t1_lapsLost
                    competitorScore.t2_score   = t2_lapsLost
                    competitorScores.append(competitorScore)
                else:
                    t1_lapsLost = 0
                    t2_lapsLost = 0


            #Add line to results array
            resultsArray.append([ result.finishPosition, result.competitor_ID, placesGainedLost, laps_off_leader, t1_pos_points, t1_fLap, t1_disqualified, t1_PlacesGainedLost, t1_lapsLost, t2_pos_points, t2_fLap, t2_disqualified, t2_PlacesGainedLost, t2_lapsLost ])



        #end For result in resultset

        print('new records count = ', len(competitorScores))
        if len(competitorScores) > 0:
            batch = 100
            CompetitorScore.objects.bulk_create(competitorScores, batch)



        #3. Go to players teams and find all players with this driver in T1

        #4. Create a PlayerScore record for each player for each competitor_score

        #5. Mark scoring event page as marked
        #6  Save array to ScoringEvent table




        toc = time.perf_counter()
        time_taken = round(toc - tic,4)
        print('Time taken - ',time_taken)

        #Create New Page with Summary Data
        scoringevents = ScoringEvent.objects.all().order_by('startDateTime')[:10]
        return render(request, 'season/score_events.html',{'scoringevents': scoringevents,'EventName':EventName, 'resultsArray':resultsArray})


    else:
        #Create Blank Page
        scoringevents = ScoringEvent.objects.all().order_by('startDateTime')[:10]
        return render(request, 'season/score_events.html',{'scoringevents': scoringevents,})









##############################################################################################
def addresults(request):
    return render(request, 'season/add_results.html')























######################################################
