from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from .models import Competitor, Event, ScoringEvent, Result, TeamProfile, AcademyScoringMatrix, CompetitorScore, TeamScore, Parameter
from django.contrib.auth.decorators import login_required
from .forms import EventForm, TeamProfileForm, TeamProfileForm
from django.contrib.auth.models import User
from django.db.models import Sum, Count
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
def leagueposition(request):

    league_list = TeamProfile.objects.all().order_by('-points_total')
    return render(request, 'season/leagueposition.html', {'league_list':league_list})


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
        pers_data = Competitor.objects.filter(surname=per)
        showPersonal = "show"
    except:
        pers_data = list(competitors[:1])
        showPersonal = " "

    return render(request, 'season/tables.html', {'personality':pers_data, 'competitors': competitors,'formulaname':formulaname, 'formula':formula, 'showPersonal':showPersonal})


####################################
def scoring(request):
    return render(request, 'season/scoring.html')




############################### USER PAGES ###################################################

@login_required
##### SHOW AND EDIT MY TEAM ##################################################################
def teamview(request):
    returnmessage = ""

    if(request.method == "POST"):
        # Go find the record we want to update
        recordtoedit = TeamProfile.objects.get(pk=request.user.team.id) # still using our 1to1 field relation

########## ToDo - SAVE OLD VERSION TO ARCHIVE ###

        # Check whether we are in a Scoring Event weekend ##
        updateallowed = get_object_or_404(Parameter, name = 'update_team_allowed').value


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
            elif ( updateallowed == "NO" ):
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
            elif ( updateallowed == "NO" ):
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
            elif ( updateallowed == "NO" ):
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
            elif ( updateallowed == "NO" ):
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
        data = data[1].split('-')
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
        score_data.append( [  data[0], data[1], score.teamPosition, type, score.academyPoints   ] )
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
        scores_dict.update( {team.id: \
            {   "name" : team.teamName, \
                "points_f1"    : 0, \
                "points_f2"    : 0, \
                "points_f3"    : 0, \
                "points_ws"    : 0,  \
                "points_total" : 0 \
             }})

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

    # Finally put league position into tem records so we can find 5 above and below
    league_list = TeamProfile.objects.all().order_by('-points_total')
    place = 1
    for team in league_list:
        team_details = team
        team_details.league_position = place
        team_details.save()
        place = place+1

    #Just to check - compare total points in competitorScores with total points in cometitor table
    tcheck = TeamProfile.objects.aggregate(team_points = Sum('points_total'))
    scheck = TeamScore.objects.aggregate(score_points = Sum('academyPoints'))

    message_2   = 'Points in team table = ' + str(tcheck['team_points']) + ' versus points in scores table = ' + str(scheck['score_points'])

    # Close timer
    toc = time.perf_counter()
    time_taken = round(toc - tic,4)

    message_3 = 'Time taken : ' + str(time_taken) + ' seconds'

    return render(request, 'season/rebuildleagues.html', {'message': message, 'message_2': message_2, 'message_3': message_3})



##############################################################################################################
##############################################################################################################


                       #############      ###            #######          ###
                             ##         #######          ##    ##       #######
                             ##        ##     ##         ##     ##     ##     ##
                             ##        ##     ##    ##   ##     ##     ##     ##
                             ##        ##     ##         ##     ##     ##     ##
                             ##         #######          ##    ##       #######
                             ##           ###            #######          ###

##############################################################################################################
##############################################################################################################

@login_required
##############################################################################################
def test(request):
    return render(request, 'season/test.html')



















######################################################
