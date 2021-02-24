from django.db import models
from django.contrib.auth.models import User


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
    mugshot                = models.ImageField(upload_to='mugshots/', default="siteimages/blankUser.png")
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
    webLink                = models.CharField(max_length=30, blank=True)
    instaHandle            = models.CharField(max_length=30, blank=True)
    twitterHandle          = models.CharField(max_length=30, blank=True)
    short_bio              = models.TextField(default = " ", blank=True)

    def __str__(self):
        return self.firstname + " " + self.surname

    class Meta:
        # Add verbose name
        verbose_name = 'Driver or Manager'
        ordering = ('-value',)

# Create your models here.
class TeamProfile(models.Model):
    user_ID                = models.OneToOneField(User, on_delete = models.CASCADE, related_name='team')
    teamName               = models.CharField(max_length=30, default='My Team')
    teamLogo               = models.ImageField(upload_to='mugshots/', default="siteimages/car_outline.jpg")
    dateStarted            = models.DateField(auto_now=True)
    dateSelected           = models.DateTimeField(auto_now=True)
    p1_1                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p1_1')
    p1_1_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p1_2                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p1_2')
    p1_2_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p1_m                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p1_m')
    p1_m_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p2_1                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p2_1')
    p2_1_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p2_2                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p2_2')
    p2_2_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p2_m                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p2_m')
    p2_m_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p3_1                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p3_1')
    p3_1_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p3_2                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p3_2')
    p3_2_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    p3_m                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='p3_m')
    p3_m_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    pw_1                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='pw_1')
    pw_1_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    pw_2                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='pw_2')
    pw_2_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    pw_m                   = models.ForeignKey(Competitor , null=True, on_delete = models.SET_NULL, related_name='pw_m')
    pw_m_cost              = models.DecimalField(max_digits=4, decimal_places=1, default = 0)


    def __str__(self):
        return self.user_ID.username + " - " + self.teamName

class TeamMember(models.Model):
    POSITION = (
    ('1_1', 'F1 Lead Driver'),
    ('1_2', 'F1 Second Driver'),
    ('1_M', 'F1 Manager'),
    ('2_1', 'F2 Lead Driver'),
    ('2_2', 'F2 Second Driver'),
    ('2_M', 'F2 Manager'),
    ('3_1', 'F3 Lead Driver'),
    ('3_2', 'F3 Second Driver'),
    ('3_M', 'F3 Manager'),
    ('W_1', 'W Lead Driver'),
    ('W_2', 'W Second Driver'),
    ('W_M', 'W Manager'),
    )
    team_ID                = models.ForeignKey(TeamProfile, null=True, on_delete = models.CASCADE, related_name='team')
    competitor_ID          = models.ForeignKey(Competitor , null=True, on_delete = models.PROTECT, related_name='member')
    position               = models.CharField(max_length=3, choices=POSITION)
    dateSelected           = models.DateTimeField(auto_now=True)


class Event(models.Model):
    name                 = models.CharField(max_length=50)
    date                 = models.DateField(auto_now=False, auto_now_add=False)
    circuit              = models.CharField(max_length=30)
    country              = models.CharField(max_length=20)
    formulas             = models.CharField(max_length=45)
    startDateTime        = models.DateTimeField(auto_now=False, auto_now_add=False)
    endDateTime          = models.DateTimeField(auto_now=False, auto_now_add=False)

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
    ('F', 'Feature Race'),
    ('S', 'Sprint Race' ),
    )
    event_ID             = models.ForeignKey(Event, null=True, on_delete = models.CASCADE, related_name='scoringEvent')
    name                 = models.CharField(max_length=40)
    formula              = models.CharField(max_length=1, choices=FORMULA)
    eventType            = models.CharField(max_length=1, choices=RACETYPE)
    startDateTime        = models.DateTimeField(auto_now=False, auto_now_add=False)

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
    competitor_ID        = models.ForeignKey(Competitor, null=True, on_delete = models.PROTECT, related_name='competitor')
    finishPosition       = models.IntegerField()
    startPosition        = models.IntegerField(default = 0)
    lapsComplete         = models.IntegerField(default = 0)
    formulaPoints        = models.IntegerField(default = 0)
    fastestLap           = models.BooleanField(default=False)
    placesGainedLost     = models.IntegerField(default = 0)

    class Meta:
        ordering = ('scoringEvent_ID',)

    def __str__(self):
        return  self.scoringEvent_ID.name + " - " + self.competitor_ID.surname + " - P" + str(self.finishPosition)

class AcademyScoringMatrix(models.Model):
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
    ('F', 'Feature Race'),
    ('S', 'Sprint Race' ),
    )
    POINTSTYPE = (
    ('P', 'Position'),
    ('F', 'Fastest Lap'),
    ('G', 'Places Gained / Lost'),
    )
    pointsType           = models.CharField(max_length=1)
    formula              = models.CharField(max_length=1, choices=FORMULA)
    role                 = models.CharField(max_length=1)
    multiplier           = models.DecimalField(max_digits=6, decimal_places=2)

class ScoringMatches(models.Model):
    player_ID            = models.ForeignKey(TeamProfile, null=True, on_delete = models.CASCADE, related_name='player')
    result_ID            = models.ForeignKey(Result, null=True, on_delete = models.CASCADE, related_name='result')
    points_Type          = models.CharField(max_length=1)
    academyPoints        = models.IntegerField()
