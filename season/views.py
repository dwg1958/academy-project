from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .models import Competitor, Event, ScoringEvent, Result, TeamProfile, AcademyScoringMatrix, CompetitorScore, TeamScore, Parameter
from django.contrib.auth.decorators import login_required
from .forms import EventForm, TeamProfileForm, TeamProfileForm
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import datetime, timedelta, time
from django.db.models import Window, F
from django.db.models.functions import DenseRank
from django.conf import settings
import time

# Create your views here.

##############################################################################################
############################### GUEST PAGES ##################################################
##############################################################################################

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
        #resultset = Result.objects.filter(scoringEvent_ID=result_id).order_by('scoringEvent_ID', 'finishPosition')
        scoringevent = ScoringEvent.objects.get(id=result_id)

        data     = scoringevent.resultsArray
        newarray = []

        data = data[2:]
        data = data[:-2]

        datarray = data.split("], [")
        for line in datarray:
            line = line.split(",")
            newline = []
            first = True
            for item in line:
                if first:
                    first = False
                else:
                    item = item.replace("<Competitor: " , "")
                    item = item.replace("Decimal('"     , "")
                    item = item.replace(">"             , "")
                    item = item.replace("')"            , "")
                    newline.append(item)

            newarray.append(newline)

        return render(request, 'season/showresults.html', {'scoringevent':scoringevent, 'newarray':newarray})

    else:
        allevents = Event.objects.all()
        return render(request, 'season/showevents.html',{'allevents':allevents})

####################################
def leaguetop20(request):

    #See if we requested a pecific league tab ("?tab=F1")
    try:
        tab = request.GET['tab']
    except:
        tab = 'overall'


    if tab == 'F1':
        order_field  = '-points_f1'
        points_field = 'points_f1'
        heading      = "Formula 1 only"
    elif tab == 'F2':
        order_field  = '-points_f2'
        points_field = 'points_f2'
        heading      = "Formula 2 only"
    elif tab == 'F3':
        order_field  = '-points_f3'
        points_field = 'points_f3'
        heading      = "Formula 3 only"
    elif tab == 'WS':
        order_field  = '-points_ws'
        points_field = 'points_ws'
        heading      = "W Series only"
    else:
        order_field  = '-points_total'
        points_field = 'points_total'
        heading      = "Overall"

    #Get Top 5
    league_list  = TeamProfile.objects.all().order_by(order_field)[:20]

    #Get my local list
    # Add the rank to each record
    ranklist = TeamProfile.objects.annotate(                                                        # add a new field to the resultset
            place=Window(                                                                           # call it 'place' and open another window on the data to find it
                expression=DenseRank(), order_by=[F(points_field).desc(),F('points_total').desc(),]  # use the rank function to order based on F1 points field
                )).filter(f1_cashpot__lt=50)                                                                                  # and if a match, use the total points to decide order


    return render(request, 'season/leaguetop20.html', {'league_list':league_list, 'heading':heading})


####################################
def tables(request):
#	textreceived = request.GET['fname']
    competitors = Competitor.objects
    return render(request, 'season/tables.html', {'competitors': competitors})


#### SHOW COMPETITOR TABLES #######
def tableformula(request, formula):

    if formula in '1234Ww':
        # Go find drivers in this formula only
        if formula == "4" or formula == "W":
            formula = "W"
            formulaname = "W Series"
        else:
            formulaname = "Formula " + formula
    else:
            formula = "1"
            formulaname = "Formula 1"

    competitors = Competitor.objects.filter(formula=formula, role="D")

    ## Find personality dataset
    try:
        per = request.GET['per']
        pers_data = Competitor.objects.get(pk=per)
        showPersonal = "show"
    except:
        pers_data = competitors.first()
        showPersonal = " "

    return render(request, 'season/tables.html', {'person':pers_data, 'competitors': competitors,'formulaname':formulaname, 'formula':formula, 'showPersonal':showPersonal})


####################################
def scoring(request):
    return render(request, 'season/scoring.html')


##############################################################################################
############################### USER PAGES ###################################################
##############################################################################################

@login_required
##############################################################################################
def monitor(request):
    return render(request, 'season/monitor.html')


@login_required
##### SHOW AND EDIT MY TEAM ##################################################################
def teamview(request):
    returnmessage = ""



    if(request.method == "POST"):
        # Go find the record we want to update
        recordtoedit = TeamProfile.objects.get(pk=request.user.team.id) # still using our 1to1 field relation

########## ToDo - SAVE OLD VERSION TO ARCHIVE ###

        # Check whether we are in a Scoring Event weekend ##
        updateallowed =  get_object_or_404(Parameter, name = 'update_team_allowed').value

        # Now change relevant fields
        if 'F1_submit' in request.POST:
            # POST arg comes in as value="1|Lewis Hamilton|29.0"
            arg1 = request.POST['p1_1_picker'] #Get arg
            arg1 = arg1[:arg1.index("|")]      #Split out the first element - the driverID
            arg2 = request.POST['p1_2_picker']
            arg2 = arg2[:arg2.index("|")]

            new_p1_1 = Competitor.objects.get(pk=arg1) #Find new driver 1 record
            new_p1_2 = Competitor.objects.get(pk=arg2)
            #check budget not exceeded and not a new team and changes allowed
            new_cash_pot = recordtoedit.f1_cashpot + recordtoedit.p1_1.value + recordtoedit.p1_2.value - new_p1_1.value - new_p1_2.value
            if ( new_cash_pot < 0 ):
                returnmessage = 'You have exceeded your budget - please choose again'
            elif ( arg1 == arg2 ):
                returnmessage = 'You have chosen the same driver twice - please choose again'
            elif ( updateallowed == 0 ):
                returnmessage = 'Sorry - No update allowed during a Scoring-Event weekend'
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
            elif ( updateallowed == 0 ):
                returnmessage = 'Sorry - No update allowed during a Scoring-Event weekend'
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
            elif ( updateallowed == 0 ):
                returnmessage = 'Sorry - No update allowed during a Scoring-Event weekend'
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
            elif ( updateallowed == 0 ):
                returnmessage = 'Sorry - No update allowed during a Scoring-Event weekend'
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
##############################################################################################
def teamscores(request):
    score_data = []
    total_score = 0
    teamdata    = TeamProfile.objects.get(pk = request.user.team.id)
    team_scores = TeamScore.objects.filter(team_ID = request.user.team.id)
    for score in team_scores:
        data = str(score.cscore_ID).split('~')
        data = data[1].split(' -')
        if score.pointsType == 'P':
            type='Finish Place'
        elif score.pointsType == 'F':
            type='Fastest Lap'
        elif score.pointsType == 'G':
            type='Places +/-'
        elif score.pointsType == 'L':
            type='LapsBehind'
        elif score.pointsType == 'D':
            type='Disqualified'
        else: type='--'
        score_data.append( [  data[0], data[1], score.teamPosition, type, score.academyPoints, score.formula  ] )
        total_score+= score.academyPoints

    return render(request, 'season/teamscores.html', {'teamdata': teamdata, 'score_data': score_data, 'total_score': total_score})


@login_required
### EDIT MY TEAM NAME ########################################################################
def teamnamepicker(request):
    if request.method == 'POST':
        team_form = TeamProfileForm(
                                    instance=request.user.team,
                                    data=request.POST,
                                    files=request.FILES)
        if team_form.is_valid():
            team_form.save()
            return redirect('teamview')
    else:
        team_form = TeamProfileForm(instance=request.user.team)
    return render(request,'season/teamnamepicker.html', {'team_form': team_form})


@login_required
####################################
def leagueposition(request):

    #See if we requested a pecific league tab ("?tab=F1")
    try:
        tab = request.GET['tab']
    except:
        tab = 'overall'


    if tab == 'F1':
        points_field   = 'points_f1'
        heading        = "F1 only"
        position_field = 'position_f1'
    elif tab == 'F2':
        points_field = 'points_f2'
        heading      = "F2 only"
        position_field = 'position_f2'
    elif tab == 'F3':
        points_field = 'points_f3'
        heading      = "F3 only"
        position_field = 'position_f3'
    elif tab == 'WS':
        points_field = 'points_ws'
        heading      = "W Series"
        position_field = 'position_ws'
    else:
        points_field = 'points_total'
        heading      = "Overall"
        position_field = 'league_position'

    #Get full league list ordered by chosen formula / overall
    full_league = TeamProfile.objects.all().order_by(position_field)

    #Get Top 5
    league_list = full_league[:5]

    #Get my local list
    # Find our position
    our_team = request.user.team
    our_position = eval('our_team.'+position_field)  #indirection!!

    # Get the 5 above and below us
    sublist = []
    for team in full_league:
        team_place = eval('team.'+position_field)
        if team_place > our_position-6 and team_place < our_position+6:
            sublist.append([team_place, team.teamLogo.url, team.teamName, team.points_f1, team.points_f2, team.points_f3, \
            team.points_ws, team.points_total, team.league_position, team.p1_1, team.p1_2, team.p2_1, team.p2_2, team.p3_1, team.p3_2, team.pw_1, team.pw_2  ])
        if team_place > our_position+6:
            break

    #Data for team position box
    events_scored = 999
    total_events  = 999
    percentile    = our_position / len(full_league) * 100

    #Package up the vbls for the position box
    boxtext = [percentile, request.user.team.teamName, our_position, events_scored, total_events]

    return render(request, 'season/leagueposition.html', {'league_list':league_list, 'sublist': sublist, 'heading':heading, 'boxtext':boxtext})


##############################################################################################
############################### ADMIN PAGES ##################################################
##############################################################################################

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
        results_calculated = False

        #Get Scoring Event details
        scoringevent_ID = int(request.GET['scoringevent'])
        scoringevent_detail = ScoringEvent.objects.get(pk=scoringevent_ID)
        EventName = scoringevent_detail.name + ' (Type:' + scoringevent_detail.eventType + ')'

        # Test if already scored and warn if it is
        if scoringevent_detail.results_in:
            scoringevents = ScoringEvent.objects.all().filter(results_in = False).order_by('startDateTime')[:10]
            return render(request, 'season/score_events.html',{'scoringevents': scoringevents,})

        # Get Scoring Matrix #############
        matrix = AcademyScoringMatrix.objects.all()
        ASM_1 = matrix.get(formula=scoringevent_detail.formula, teamPosition='1')
        ASM_2 = matrix.get(formula=scoringevent_detail.formula, teamPosition='2')
        resultsArray   = []  # Make an array to send data to table in HTML template

        #Set Event type
        if   scoringevent_detail.eventType in 'RF3':    rt = 'm_'
        elif scoringevent_detail.eventType in '12S':    rt = 's_'
        else:                                           rt = 'q_'

        #2. For each result
        resultset = Result.objects.filter(scoringEvent_ID=int(scoringevent_ID)).order_by('finishPosition')

        #Make array for new records to batch upload at the end
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
                competitorScore.result_ID       = result
                competitorScore.scoringevent_ID = int(scoringevent_ID)
                competitorScore.competitor_ID   = result.competitor_ID
                competitorScore.pointsType      = 'P'
                competitorScore.t1_score        = t1_pos_points
                competitorScore.t2_score        = t2_pos_points
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
                competitorScore.scoringevent_ID = int(scoringevent_ID)
                competitorScore.competitor_ID   = result.competitor_ID
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
                    competitorScore.scoringevent_ID = int(scoringevent_ID)
                    competitorScore.competitor_ID   = result.competitor_ID
                    competitorScore.pointsType = 'F'
                    competitorScore.t1_score   = t1_fLap
                    competitorScore.t2_score   = t2_fLap
                    competitorScores.append(competitorScore)
                else:
                    t1_fLap = t2_fLap = 0


                # Places gained/lost points
                placesGainedLost = result.placesGainedLost
                if placesGainedLost != 0:
                    var = rt + 'pos_gained'
                    t1_PlacesGainedLost = placesGainedLost * getattr(ASM_1,var)
                    t2_PlacesGainedLost = placesGainedLost * getattr(ASM_2,var)
                    # Make new competitor score record
                    competitorScore = CompetitorScore()
                    competitorScore.result_ID  = result
                    competitorScore.scoringevent_ID = int(scoringevent_ID)
                    competitorScore.competitor_ID   = result.competitor_ID
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
                    competitorScore.scoringevent_ID = int(scoringevent_ID)
                    competitorScore.competitor_ID   = result.competitor_ID
                    competitorScore.pointsType = 'L'
                    competitorScore.t1_score   = t1_lapsLost
                    competitorScore.t2_score   = t2_lapsLost
                    competitorScores.append(competitorScore)
                else:
                    t1_lapsLost = 0
                    t2_lapsLost = 0

            #Add line to results array
            resultsArray.append([ result.competitor_ID.id, result.finishPosition, result.competitor_ID,   placesGainedLost, laps_off_leader, t1_pos_points, t1_fLap, t1_disqualified, t1_PlacesGainedLost, t1_lapsLost, t2_pos_points, t2_fLap, t2_disqualified, t2_PlacesGainedLost, t2_lapsLost ])

        # Create Competitor Score records from array
        if len(competitorScores) > 0:
            results_calculated = True
            batch = 100
            CompetitorScore.objects.bulk_create(competitorScores, batch)

#############################################################################################################################
        #3. Now create team score records
        cscores = CompetitorScore.objects.filter(scoringevent_ID = int(scoringevent_ID))
        print('Cscore records found :', len(cscores))
        tscores = []

        # For each competitor score for this event
        for cscore in cscores:
            driver_ID = str(cscore.result_ID).split('~')[0]

            # Find all teams with this driver as T_1
            t1_teams = TeamProfile.objects.filter(p1_1 = driver_ID) | TeamProfile.objects.filter(p2_1 = driver_ID) | TeamProfile.objects.filter(p3_1 = driver_ID) | TeamProfile.objects.filter(pw_1 = driver_ID) #<<<<<<< ---------------  MAKE WORK FOR ALL FORMULAS
            if len(t1_teams) > 0:
                for team in t1_teams:
                    # Make team score record for each T_1 position
                    teamscore = TeamScore()
                    teamscore.team_ID          = team
                    teamscore.cscore_ID        = cscore
                    teamscore.scoringevent_ID  = int(scoringevent_ID)
                    teamscore.driver_ID        = cscore.result_ID.competitor_ID
                    teamscore.eventType        = scoringevent_detail.eventType
                    teamscore.teamPosition     = '1'
                    teamscore.formula          = scoringevent_detail.formula
                    teamscore.pointsType       = cscore.pointsType
                    teamscore.academyPoints    = cscore.t1_score
                    tscores.append(teamscore)

            # Find all teams with this driver as T_2
            t2_teams = TeamProfile.objects.filter(p1_2 = driver_ID) | TeamProfile.objects.filter(p2_2 = driver_ID) | TeamProfile.objects.filter(p3_2 = driver_ID) | TeamProfile.objects.filter(pw_2 = driver_ID)  #<<<<<<< ---------------  MAKE WORK FOR ALL FORMULAS
            if len(t2_teams) > 0:
                for team in t2_teams:
                    # Make team score record for each T_1 position
                    teamscore = TeamScore()
                    teamscore.team_ID          = team
                    teamscore.cscore_ID        = cscore
                    teamscore.scoringevent_ID  = int(scoringevent_ID)
                    teamscore.driver_ID        = cscore.result_ID.competitor_ID
                    teamscore.eventType        = scoringevent_detail.eventType
                    teamscore.teamPosition     = '2'
                    teamscore.formula          = scoringevent_detail.formula
                    teamscore.pointsType       = cscore.pointsType
                    teamscore.academyPoints    = cscore.t2_score
                    tscores.append(teamscore)

        # Create Competitor Score records from array
        if len(tscores) > 0:
            batch = 100
            TeamScore.objects.bulk_create(tscores, batch)

        ################# TO DO ################################################
        # 1. Update team_profile records with total scores for FORMULAS        #
        # 2. Update competitor records with total scores for each scoring type #
        ########################################################################


        # Mark scoring event page as marked - !!!! ALSO STOP SCORING IF TRUE  !!!!
        if results_calculated:
            scoringevent_detail.results_in = True
            # Save results array to ScoringEvent table to calendar pages
            scoringevent_detail.resultsArray = resultsArray
            scoringevent_detail.save()

            # Set team_update_on parameter back to OK (it will reset if there is another event)
            para = Parameter.objects.get(name="update_team_allowed")
            para.value = 1
            para.text = ""
            para.save()

        # Close timer
        toc = time.perf_counter()
        time_taken = round(toc - tic,4)

        #Create New Page with Summary Data
        scoringevents = ScoringEvent.objects.all().filter(results_in = False).order_by('startDateTime')[:10]
        return render(request, 'season/score_events.html',{'scoringevents': scoringevents,'EventName':EventName, 'resultsArray':resultsArray, 'time_taken':time_taken, 'crecords':len(competitorScores), 'trecords': len(tscores)})

    else:
        #Create Blank Page
        scoringevents = ScoringEvent.objects.all().filter(results_in = False).order_by('startDateTime')[:10]
        return render(request, 'season/score_events.html',{'scoringevents': scoringevents,})

@login_required
##############################################################################################
def addresults(request):

    # If event specified, ask for result details
    if "scoringevent" in request.GET:
        #Get Scoring Event details
        scoringevent = int(request.GET['scoringevent'])
        scoringevent_detail = ScoringEvent.objects.get(pk=scoringevent)
        eventName = scoringevent_detail.name + ' (Type:' + scoringevent_detail.eventType + ')'

        #Show results already in:
        resultsSoFar  = Result.objects.all().filter(scoringEvent_ID = scoringevent).order_by('finishPosition')
        driverOptions = Competitor.objects.filter(formula = scoringevent_detail.formula).filter(role = 'D')
        #remove those already selected #######################
        driversremaining = []
        for driver in driverOptions:
            try:
                present = resultsSoFar.get(competitor_ID = driver.id)
            except:
                driversremaining.append(driver)

        # If no drivers left to choose then go back to blank chooser screen
        if len(driversremaining) == 0:
            #First Screen - Choose an event
            scoringevents = ScoringEvent.objects.all().filter(results_in = False).order_by('startDateTime')[:10]
            return render(request, 'season/add_results.html',{'scoringevents': scoringevents})

        nextpos = len(resultsSoFar)+1
        return render(request, 'season/add_results.html',{'eventName': eventName, 'event':scoringevent_detail, 'resultsSoFar':resultsSoFar, 'driverOptions':driversremaining, 'nextpos':nextpos})


    #If new record details sent, save them:
    elif request.method == 'POST':
        #Get Scoring Event details
        scoringevent_detail = ScoringEvent.objects.get( pk=int(request.POST['event_id']) )
        driver_detail       = Competitor.objects.get( pk=int(request.POST['driver']))

        #Save new result record
        newResult = Result()
        newResult.scoringEvent_ID  = scoringevent_detail
        newResult.competitor_ID    = driver_detail
        newResult.finishPosition   = int(request.POST['finishPosition'])
        #disqualified checkbox does not return if not set, so look whether it exists..
        disqualified = request.POST.get('disqualified')
        newResult.disqualified     = True if disqualified else False


        if scoringevent_detail.eventType == 'Q':
            print('Qualifying')
        else:
            newResult.startPosition    = int(request.POST['startPosition'])
            newResult.laps_off_leader  = int(request.POST['lapsOffLeader'])
            newResult.formulaPoints    = 0
            newResult.placesGainedLost = int(request.POST['startPosition']) - int(request.POST['finishPosition'])
            #fastestLap checkbox does not return if not set, so look whether it exists..
            fastestLap = request.POST.get('fastestLap')
            newResult.fastestLap     = True if fastestLap else False

        newResult.save()

        resultsSoFar    = Result.objects.all().filter(scoringEvent_ID = scoringevent_detail.id).order_by('finishPosition')
        driverOptions = Competitor.objects.filter(formula = scoringevent_detail.formula).filter(role = 'D')
        #remove those already selected #######################
        driversremaining = []
        for driver in driverOptions:
            try:
                present = resultsSoFar.get(competitor_ID = driver.id)
            except:
                driversremaining.append(driver)

        # If no drivers left to choose then go back to blank chooser screen
        if len(driversremaining) == 0:
            #First Screen - Choose an event
            scoringevents = ScoringEvent.objects.all().filter(results_in = False).order_by('startDateTime')[:10]
            return render(request, 'season/add_results.html',{'scoringevents': scoringevents})

        nextpos = len(resultsSoFar)+1
        eventName = scoringevent_detail.name + ' (Type:' + scoringevent_detail.eventType + ')'

        #Show results already in:
        resultsSoFar = Result.objects.all().filter(scoringEvent_ID = scoringevent_detail.id).order_by('finishPosition')
        return render(request, 'season/add_results.html',{'eventName': eventName, 'event':scoringevent_detail, 'resultsSoFar':resultsSoFar, 'driverOptions':driversremaining, 'nextpos':nextpos})

    else:
        #First Screen - Choose an event
        scoringevents = ScoringEvent.objects.all().filter(results_in = False).order_by('startDateTime')[:10]
        return render(request, 'season/add_results.html',{'scoringevents': scoringevents})


@login_required
##############################################################################################
def rebuildleagues(request):


    #Start Timer
    tic = time.perf_counter()

    scores_dict  = {}

    #create the dictionary
    alldrivers = Competitor.objects.filter(role ='D')
    for driver in alldrivers:
        scores_dict.update({driver.id: {"name" : driver.firstname +' '+  driver.surname, "pos_points" : 0, "fl_points" : 0, "pgl_points" : 0, "lbl_points" : 0, "dsq_points" : 0 }})

    #Get position Points
    #resultset = Competitor.objects.filter(cscore_driver__pointsType ='P').filter(formula ='1').annotate(pos_points = Sum('cscore_driver__t2_score')).order_by('firstname')#.distinct()
    resultset = Competitor.objects.filter(cscore_driver__pointsType ='P').filter(role ='D').annotate(pos_points = Sum('cscore_driver__t2_score')).order_by('firstname')#.distinct()
    for driver in resultset:
        scores_dict[driver.id]['pos_points'] = driver.pos_points

    #Get fastestLap Points
    resultset = Competitor.objects.filter(cscore_driver__pointsType ='F').filter(role ='D').annotate(fl_points = Sum('cscore_driver__t2_score')).order_by('firstname').distinct()
    for driver in resultset:
        scores_dict[driver.id]['fl_points'] = driver.fl_points

    #Get placesGainedLostG Points
    resultset = Competitor.objects.filter(cscore_driver__pointsType ='G').filter(role ='D').annotate(pgl_points = Sum('cscore_driver__t2_score')).order_by('firstname').distinct()
    for driver in resultset:
        scores_dict[driver.id]['pgl_points'] = driver.pgl_points

    #Get LapsBehindLeader Points
    resultset = Competitor.objects.filter(cscore_driver__pointsType ='L').filter(role ='D').annotate(lbl_points = Sum('cscore_driver__t2_score')).order_by('firstname').distinct()
    for driver in resultset:
        scores_dict[driver.id]['lbl_points'] = driver.lbl_points

    #Get Disqualification Points
    resultsetD = Competitor.objects.filter(cscore_driver__pointsType ='D').filter(role ='D').annotate(dsq_points = Sum('cscore_driver__t2_score')).order_by('firstname').distinct()
    for driver in resultsetD:
        scores_dict[driver.id]['dsq_points'] = driver.dsq_points

    #Print out dictionaries:
    #for x in scores_dict:
    #    print(scores_dict[x])
    #    print(scores_dict[x].values())

    # Now work through drivers and insert points
    for driver in alldrivers:
        driver_record = driver
        driver_record.points_pos   = scores_dict[driver.id]['pos_points']
        driver_record.points_fl    = scores_dict[driver.id]['fl_points']
        driver_record.points_pgl   = scores_dict[driver.id]['pgl_points']
        driver_record.points_lbl   = scores_dict[driver.id]['lbl_points']
        driver_record.points_dsq   = scores_dict[driver.id]['dsq_points']
        driver_record.points_total = scores_dict[driver.id]['pos_points'] + scores_dict[driver.id]['fl_points'] + scores_dict[driver.id]['pgl_points']+ scores_dict[driver.id]['lbl_points'] + scores_dict[driver.id]['dsq_points']
        driver_record.save()

    #Just to check - compare total points in competitorScores with total points in cometitor table
    ccheck = Competitor.objects.filter(role ='D').aggregate(driver_points = Sum('points_total'))
    scheck = CompetitorScore.objects.aggregate(score_points = Sum('t2_score'))
    message   = 'Points in drivers table = ' + str(ccheck['driver_points']) + ' versus points in scores table = ' + str(scheck['score_points'])

    # Aggregate team scores for formulae ############################

    scores_dict  = {}

    #create the dictionary
    allteams = TeamProfile.objects.all()
    for team in allteams:
        scores_dict.update( {team.id:   \
            {   "name" : team.teamName, \
                "points_f1"    : 0,     \
                "points_f2"    : 0,     \
                "points_f3"    : 0,     \
                "points_ws"    : 0,     \
                "points_total" : 0      \
             }})

    league_total_teams  =  len(allteams)

    #Get scores
    resultset = TeamProfile.objects.filter(team__formula = '1').annotate(f1_points = Sum('team__academyPoints')).distinct()
    for driver in resultset:
        scores_dict[driver.id]['points_f1'] = driver.f1_points

    resultset = TeamProfile.objects.filter(team__formula = '2').annotate(f2_points = Sum('team__academyPoints')).distinct()
    for driver in resultset:
        scores_dict[driver.id]['points_f2'] = driver.f2_points

    resultset = TeamProfile.objects.filter(team__formula = '3').annotate(f3_points = Sum('team__academyPoints')).distinct()
    for driver in resultset:
        scores_dict[driver.id]['points_f3'] = driver.f3_points

    resultset = TeamProfile.objects.filter(team__formula = 'W').annotate(ws_points = Sum('team__academyPoints')).distinct()
    for driver in resultset:
        scores_dict[driver.id]['points_ws'] = driver.ws_points

    # Now work through teams and insert points
    for team in allteams:
        team_record = team
        team_record.points_f1    = scores_dict[team.id]['points_f1']
        team_record.points_f2    = scores_dict[team.id]['points_f2']
        team_record.points_f3    = scores_dict[team.id]['points_f3']
        team_record.points_ws    = scores_dict[team.id]['points_ws']
        team_record.points_total = scores_dict[team.id]['points_f1'] + scores_dict[team.id]['points_f2'] + scores_dict[team.id]['points_f3']+ scores_dict[team.id]['points_ws']
        team_record.save()

###################### ADD POSITIONS TO TEAM RECORDS #################################################


    # Finally put league position into team records so we can find 5 above and below
    league_list = TeamProfile.objects.all().order_by('-points_total')
    place = 1
    for team in league_list:
        team_details = team
        team_details.league_position = place
        team_details.save()
        place = place+1

    # Repeat for F1
    league_list = TeamProfile.objects.all().order_by('-points_f1', '-points_total')
    place = 1
    for team in league_list:
        team_details = team
        team_details.position_f1 = place
        team_details.save()
        place = place+1

    # Repeat for F2
    league_list = TeamProfile.objects.all().order_by('-points_f2', '-points_total')
    place = 1
    for team in league_list:
        team_details = team
        team_details.position_f2 = place
        team_details.save()
        place = place+1

    # Repeat for F3
    league_list = TeamProfile.objects.all().order_by('-points_f3', '-points_total')
    place = 1
    for team in league_list:
        team_details = team
        team_details.position_f3 = place
        team_details.save()
        place = place+1

    # Repeat for WS
    league_list = TeamProfile.objects.all().order_by('-points_ws', '-points_total')
    place = 1
    for team in league_list:
        #print(place , "  " , team.points_ws, "  " ,team.points_total, "  " ,team.teamName)
        team_details = team
        team_details.position_ws = place
        team_details.save()
        place = place+1




###################### [END] ADD POSITIONS TO TEAM RECORDS ############################################

    # Update parameter totals for static reports
    para = Parameter.objects.get(name="league_total_teams")
    para.value = league_total_teams
    para.save()


    #Just to check - compare total points in competitorScores with total points in cometitor table
    tcheck = TeamProfile.objects.aggregate(team_points = Sum('points_total'))
    scheck = TeamScore.objects.aggregate(score_points = Sum('academyPoints'))

    message_2   = 'Points in team table = ' + str(tcheck['team_points']) + ' versus points in scores table = ' + str(scheck['score_points'])

    # Close timer
    toc = time.perf_counter()
    time_taken = round(toc - tic,4)

    message_3 = 'Time taken : ' + str(time_taken) + ' seconds'

    return render(request, 'season/rebuildleagues.html', {'message': message, 'message_2': message_2, 'message_3': message_3})


##############################################################################################
##############################################################################################


                   #############      ###            #######          ###
                         ##         #######          ##    ##       #######
                         ##        ##     ##         ##     ##     ##     ##
                         ##        ##     ##    ##   ##     ##     ##     ##
                         ##        ##     ##         ##     ##     ##     ##
                         ##         #######          ##    ##       #######
                         ##           ###            #######          ###

##############################################################################################
##############################################################################################

@login_required
##############################################################################################
def test(request):

    print(settings.DG_CATEGORIES)

######################################  TO DO - PUT THESE INTO PARAMETERS #########################################

    total_events = ScoringEvent.objects.all().count()
    print("total_events = ", total_events)

    All_events_in = ScoringEvent.objects.filter(results_in=True).count()
    print('All_events_in = ', All_events_in)

    F1_events = ScoringEvent.objects.filter(formula = '1').count()
    print("F1_events = ", F1_events)

    F1_results_in = ScoringEvent.objects.filter(formula = '1').filter(results_in=True).count()
    print('F1_results_in = ', F1_results_in)


    return render(request, 'season/test.html')#, {'league_list': sublist, "heading":heading})

######################################  PUT THESE INTO PARAMETERS #################################################


















################################################################################################
