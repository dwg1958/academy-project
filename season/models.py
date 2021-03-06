from django.db import models
from django.contrib.auth.models import User
from .formatChecker import ContentTypeRestrictedFileField


class Parameter(models.Model):
    name                = models.CharField(max_length=20)
    explanation         = models.CharField(max_length=40,  blank=True)
    value               = models.IntegerField(default = 0)
    text                = models.CharField(max_length=60,  blank=True)
    long_text           = models.TextField(default = " ",  blank=True)

    def __str__(self):
        return self.name

class Competitor(models.Model):
    FORMULA = (
    ('1', 'Formula 1'),
    ('2', 'Formula 2'),
    ('3', 'Formula 3'),
    ('W', 'W Series' ),
    )
    ROLE = (
    ('D', 'Driver'),
    ('M', 'Manager'),
    )
    #mugshot                = models.ImageField(upload_to='mugshots/', default="siteimages/blankUser.png")
    mugshot                = ContentTypeRestrictedFileField(upload_to='mugshots/', default="siteimages/blankUser.png")
    surname                = models.CharField(max_length=20)
    firstname              = models.CharField(max_length=20)
    role                   = models.CharField(max_length=1, choices=ROLE)
    formula                = models.CharField(max_length=1, choices=FORMULA)
    team                   = models.CharField(max_length=20, blank=True)
    value                  = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    nationality            = models.CharField(max_length=20, blank=True)
    championships          = models.IntegerField(default = 0)
    pointsPreviousSeasons  = models.IntegerField(default = 0)
    winsPreviousSeasons    = models.IntegerField(default = 0)
    polesPreviousSeasons   = models.IntegerField(default = 0)
    pointsThisSeason       = models.IntegerField(default = 0)
    winsThisSeason         = models.IntegerField(default = 0)
    polesThisSeason        = models.IntegerField(default = 0)
    gainLossThisseason     = models.IntegerField(default = 0)
    fastestLapsThisSeason  = models.IntegerField(default = 0)
    previousHistory        = models.CharField(max_length=200, blank=True)
    webLink                = models.CharField(max_length=30,  blank=True)
    instaHandle            = models.CharField(max_length=30,  blank=True)
    twitterHandle          = models.CharField(max_length=30,  blank=True)
    short_bio              = models.TextField(default = " ",  blank=True)
    points_total           = models.DecimalField(max_digits=5, decimal_places=1, default = 0)
    points_pos             = models.DecimalField(max_digits=5, decimal_places=1, default = 0)
    points_fl              = models.DecimalField(max_digits=5, decimal_places=1, default = 0)
    points_pgl             = models.DecimalField(max_digits=5, decimal_places=1, default = 0)
    points_lbl             = models.DecimalField(max_digits=5, decimal_places=1, default = 0)
    points_dsq             = models.DecimalField(max_digits=5, decimal_places=1, default = 0)

    def __str__(self):
        return self.firstname + " " + self.surname

    class Meta:
        # Add verbose name
        verbose_name = 'Driver'
        ordering = ('-value',)

# Create your models here.
class TeamProfile(models.Model):
    user_ID                = models.OneToOneField(User, on_delete = models.CASCADE, related_name='team')
    teamName               = models.CharField(max_length=30, default='My Team')
    #teamLogo               = models.ImageField(upload_to='mugshots/', default="siteimages/defaultTeam.png")
    teamLogo               = ContentTypeRestrictedFileField(upload_to='mugshots/', default="siteimages/defaultTeam.png")
    dateStarted            = models.DateField(auto_now=True)
    dateSelected           = models.DateTimeField(auto_now=True)
    f1_cashpot             = models.DecimalField(max_digits=4, decimal_places=1, default = 50.0)
    f2_cashpot             = models.DecimalField(max_digits=4, decimal_places=1, default = 30.0)
    f3_cashpot             = models.DecimalField(max_digits=4, decimal_places=1, default = 20.0)
    ws_cashpot             = models.DecimalField(max_digits=4, decimal_places=1, default = 20.0)
    p1_1                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p1_1', default=1)
    p1_1_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p1_2                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p1_2', default=1)
    p1_2_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p1_m                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p1_m', default=1)
    p1_m_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p2_1                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p2_1', default=1)
    p2_1_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p2_2                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p2_2', default=1)
    p2_2_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p2_m                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p2_m', default=1)
    p2_m_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p3_1                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p3_1', default=1)
    p3_1_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p3_2                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p3_2', default=1)
    p3_2_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p3_m                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p3_m', default=1)
    p3_m_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    pw_1                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='pw_1', default=1)
    pw_1_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    pw_2                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='pw_2', default=1)
    pw_2_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    pw_m                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='pw_m', default=1)
    pw_m_cost              = models.DecimalField(max_digits=5, decimal_places=1, default = 0)
    points_total           = models.DecimalField(max_digits=5, decimal_places=1, default = 0)
    points_f1              = models.DecimalField(max_digits=5, decimal_places=1, default = 0)
    points_f2              = models.DecimalField(max_digits=5, decimal_places=1, default = 0)
    points_f3              = models.DecimalField(max_digits=5, decimal_places=1, default = 0)
    points_ws              = models.DecimalField(max_digits=5, decimal_places=1, default = 0)
    league_position        = models.IntegerField(default=0)
    position_f1            = models.IntegerField(default=0)
    position_f2            = models.IntegerField(default=0)
    position_f3            = models.IntegerField(default=0)
    position_ws            = models.IntegerField(default=0)

    def __str__(self):
        return self.teamName

    class Meta:
        ordering = ('-points_total',)


class Event(models.Model):
    name                 = models.CharField(max_length=50)
    round                = models.IntegerField(default=0)
    date                 = models.DateField(auto_now=False, auto_now_add=False)
    circuit              = models.CharField(max_length=30)
    country              = models.CharField(max_length=20)
    tla                  = models.CharField(max_length=3, default = "")
    formulas             = models.CharField(max_length=45)
    startDateTime        = models.DateTimeField(auto_now=False, auto_now_add=False)
    endDateTime          = models.DateTimeField(auto_now=False, auto_now_add=False)
    topF1DriverScore     = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    topF2DriverScore     = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    topF3DriverScore     = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    topWSDriverScore     = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    topTeamScore         = models.DecimalField(max_digits=6, decimal_places=2, default = 0)

    class Meta:
        ordering = ('date',)

    def __str__(self):
        return self.name

    #def eventDate_Pretty(self):
    #    return Event.date.strftime('%b %e, %Y')

class ScoringEvent(models.Model):
    FORMULA = (
    ('1', 'Formula 1'),
    ('2', 'Formula 2'),
    ('3', 'Formula 3'),
    ('W', 'W Series' ),
    )
    RACETYPE = (
    ('Q', 'Qualifying'),
    ('R', 'Race'),
    ('1', 'Race 1'),
    ('2', 'Race 2' ),
    ('3', 'Race 3' ),
    ('F', 'Feature Race'),
    ('S', 'Sprint Race' ),
    )
    event_ID             = models.ForeignKey(Event, null=True, on_delete = models.CASCADE, related_name='scoringEvent')
    name                 = models.CharField(max_length=40)
    formula              = models.CharField(max_length=1, choices=FORMULA)
    eventType            = models.CharField(max_length=1, choices=RACETYPE)
    startDateTime        = models.DateTimeField(auto_now=False, auto_now_add=False)
    results_in           = models.BooleanField(default=False)
    resultsArray         = models.TextField(default="-")

    class Meta:
        ordering = ('formula','startDateTime',)

    def __str__(self):
        return self.name

    def get_eventType(self):
        return [i[1] for i in ScoringEvent._meta.get_field('eventType').choices if i[0] == self.eventType][0]

    #def scoringEventDate_Pretty(self):
        #return ScoringEvent.startDateTime.strftime('%A, %b %e, %Y at %-H:%M')

class Result(models.Model):
    scoringEvent_ID      = models.ForeignKey(ScoringEvent, null=True, on_delete = models.CASCADE, related_name='result')
    competitor_ID        = models.ForeignKey(Competitor, null=True, on_delete = models.DO_NOTHING, related_name='competitor')
    finishPosition       = models.IntegerField()
    startPosition        = models.IntegerField(default = 0)
    laps_off_leader      = models.IntegerField(default = 0)
    formulaPoints        = models.IntegerField(default = 0)
    placesGainedLost     = models.IntegerField(default = 0)
    fastestLap           = models.BooleanField(default=False)
    disqualified         = models.BooleanField(default=False)

    class Meta:
        ordering = ('scoringEvent_ID',)

    def __str__(self):
        return  str(self.competitor_ID.id) + "~" +self.scoringEvent_ID.name + " - " + self.competitor_ID.firstname + " " + self.competitor_ID.surname + " - P" + str(self.finishPosition)

class CompetitorScore(models.Model):
    POINTSTYPE = (
    ('P', 'Position'),
    ('F', 'Fastest Lap'),
    ('G', 'Places Gained / Lost'),
    ('L', 'Laps Behind Leader'),
    ('D', 'Disqualification'),
    )
    result_ID       = models.ForeignKey(Result, null=True, on_delete = models.CASCADE, related_name='result')
    competitor_ID   = models.ForeignKey(Competitor, null=True, on_delete = models.DO_NOTHING, related_name='cscore_driver')
    scoringevent_ID = models.IntegerField(default = 0)
    pointsType      = models.CharField(max_length=1, choices=POINTSTYPE)
    t1_score        = models.DecimalField(max_digits=6, decimal_places=2)
    t2_score        = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return  str(self.result_ID.competitor_ID.id)+ ' ~ ' + self.result_ID.competitor_ID.firstname + ' ' + self.result_ID.competitor_ID.surname + " - " + self.result_ID.scoringEvent_ID.name + " - T1:" + str(self.t1_score) + " - T2:" + str(self.t2_score)

class TeamScore(models.Model):
    TEAMPOSITION = (
    ('1', '1. Lead Driver'),
    ('2', '2. Second Driver'),
    )
    POINTSTYPE = (
    ('P', 'Position'),
    ('F', 'Fastest Lap'),
    ('G', 'Places Gained / Lost'),
    ('L', 'Laps Behind Leader'),
    ('D', 'Disqualification'),
    )
    EVENTTYPE = (
    ('Q', 'Qualifying'),
    ('R', 'Race'),
    ('1', 'Race 1'),
    ('2', 'Race 2' ),
    ('3', 'Race 3' ),
    ('F', 'Feature Race'),
    ('S', 'Sprint Race' ),
    )
    team_ID              = models.ForeignKey(TeamProfile, null=True, on_delete = models.CASCADE, related_name='team')
    cscore_ID            = models.ForeignKey(CompetitorScore, null=True, on_delete = models.CASCADE, related_name='cscore')
    scoringevent_ID      = models.IntegerField(default = 0)
    driver_ID            = models.ForeignKey(Competitor, null=True, on_delete = models.DO_NOTHING, related_name='driver')
    eventType            = models.CharField(max_length=1, choices=EVENTTYPE, default='Q')
    teamPosition         = models.CharField(max_length=1, choices=TEAMPOSITION)
    formula              = models.CharField(max_length=1, default = '1')
    pointsType           = models.CharField(max_length=1, choices=POINTSTYPE)
    academyPoints        = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return  self.team_ID.teamName + " - PT:" + self.pointsType

class AcademyScoringMatrix(models.Model):
    FORMULA = (
    ('1', 'Formula 1'),
    ('2', 'Formula 2'),
    ('3', 'Formula 3'),
    ('W', 'W Series' ),
    )
    TEAMPOSITION = (
    ('1', '1. Lead Driver'),
    ('2', '2. Second Driver'),
    )

    formula             = models.CharField(max_length=1, choices=FORMULA)
    teamPosition        = models.CharField(max_length=1, choices=TEAMPOSITION, default = '1')
    q_1                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    q_2                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    q_3                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    q_4                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    q_5                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    q_6                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    q_7                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    q_8                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    q_9                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    q_10                = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    q_disqualified      = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    m_1                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    m_2                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    m_3                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    m_4                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    m_5                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    m_6                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    m_7                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    m_8                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    m_9                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    m_10                = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    m_fastest_lap       = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    m_pos_gained        = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    m_laps_off_leader   = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    m_disqualified      = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    s_1                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    s_2                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    s_3                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    s_4                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    s_5                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    s_6                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    s_7                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    s_8                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    s_9                 = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    s_10                = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    s_fastest_lap       = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    s_pos_gained        = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    s_laps_off_leader   = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    s_disqualified      = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)

    def __str__(self):
        return  self.formula + " - " + self.teamPosition


class TeamArchive(models.Model):
    user_ID                = models.ForeignKey(User, on_delete = models.DO_NOTHING, related_name='archive')
    teamName               = models.CharField(max_length=30, default='My Team Archive')
    dateSelected           = models.DateTimeField(auto_now=True)
    f1_cashpot             = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    f2_cashpot             = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    f3_cashpot             = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    ws_cashpot             = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p1_1                   = models.ForeignKey(Competitor , null=True, on_delete = models.DO_NOTHING, related_name='a_p1_1', default=1)
    p1_1_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p1_2                   = models.ForeignKey(Competitor , null=True, on_delete = models.DO_NOTHING, related_name='a_p1_2', default=1)
    p1_2_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p1_m                   = models.ForeignKey(Competitor , null=True, on_delete = models.DO_NOTHING, related_name='a_p1_m', default=1)
    p1_m_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p2_1                   = models.ForeignKey(Competitor , null=True, on_delete = models.DO_NOTHING, related_name='a_p2_1', default=1)
    p2_1_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p2_2                   = models.ForeignKey(Competitor , null=True, on_delete = models.DO_NOTHING, related_name='a_p2_2', default=1)
    p2_2_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p2_m                   = models.ForeignKey(Competitor , null=True, on_delete = models.DO_NOTHING, related_name='a_p2_m', default=1)
    p2_m_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p3_1                   = models.ForeignKey(Competitor , null=True, on_delete = models.DO_NOTHING, related_name='a_p3_1', default=1)
    p3_1_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p3_2                   = models.ForeignKey(Competitor , null=True, on_delete = models.DO_NOTHING, related_name='a_p3_2', default=1)
    p3_2_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p3_m                   = models.ForeignKey(Competitor , null=True, on_delete = models.DO_NOTHING, related_name='a_p3_m', default=1)
    p3_m_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    pw_1                   = models.ForeignKey(Competitor , null=True, on_delete = models.DO_NOTHING, related_name='a_pw_1', default=1)
    pw_1_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    pw_2                   = models.ForeignKey(Competitor , null=True, on_delete = models.DO_NOTHING, related_name='a_pw_2', default=1)
    pw_2_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    pw_m                   = models.ForeignKey(Competitor , null=True, on_delete = models.DO_NOTHING, related_name='a_pw_m', default=1)
    pw_m_cost              = models.DecimalField(max_digits=5, decimal_places=1, default = 0)
    points_total           = models.DecimalField(max_digits=5, decimal_places=1, default = 0)

    def __str__(self):
        return self.teamName


class DriverWeekendScore(models.Model):
    FORMULA = (
    ('1', 'Formula 1'),
    ('2', 'Formula 2'),
    ('3', 'Formula 3'),
    ('W', 'W Series' ),
    )
    driver_ID           = models.ForeignKey(Competitor, null=True, on_delete = models.DO_NOTHING)
    formula             = models.CharField(max_length=1, choices=FORMULA)
    weekend             = models.ForeignKey(Event, null=True, on_delete = models.DO_NOTHING)
    points_this_weekend = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    posn_this_weekend   = models.IntegerField(default = 0)


class TeamWeekendScore(models.Model):
    team_ID               = models.ForeignKey(TeamProfile, null=True, on_delete = models.DO_NOTHING)
    weekend               = models.ForeignKey(Event, null=True, on_delete = models.DO_NOTHING)
    points_f1             = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    points_f2             = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    points_f3             = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    points_ws             = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    points_total          = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    position_f1           = models.IntegerField(default = 0)
    position_f2           = models.IntegerField(default = 0)
    position_f3           = models.IntegerField(default = 0)
    position_ws           = models.IntegerField(default = 0)
    position_total        = models.IntegerField(default = 0)
    points_f1_since       = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    points_f2_since       = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    points_f3_since       = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    points_ws_since       = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    points_total_since    = models.DecimalField(max_digits=6, decimal_places=2, default = 0)
    position_f1_since     = models.IntegerField(default = 0)
    position_f2_since     = models.IntegerField(default = 0)
    position_f3_since     = models.IntegerField(default = 0)
    position_ws_since     = models.IntegerField(default = 0)
    position_total_since  = models.IntegerField(default = 0)
