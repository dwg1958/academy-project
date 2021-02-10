from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TeamProfile(models.Model):
    user_ID                = models.OneToOneField(User, on_delete = models.CASCADE)
    teamName               = models.CharField(max_length=20)
    teamLogo               = models.ImageField(upload_to='mugshots/', default="siteimages/blankUser.png")
    dateStarted            = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.user_ID.username + " - " + self.teamName

class Competitor(models.Model):
    FORMULA = (
    ('1', 'Formula 1'),
    ('2', 'Formula 2'),
    ('3', 'Formula 3'),
    ('W', 'W Series' ),
    )
    mugshot                = models.ImageField(upload_to='mugshots/')
    surname                = models.CharField(max_length=20)
    firstname              = models.CharField(max_length=20)
    role                   = models.CharField(max_length=1, default = 'D')
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

    #def birthday_pretty(self):
    #    return self.birthdate.strftime('%b %e, %Y')

class Event(models.Model):
    name                 = models.CharField(max_length=40)
    date                 = models.DateField(auto_now=False, auto_now_add=False)
    circuit              = models.CharField(max_length=20)
    country              = models.CharField(max_length=20)
    formulas             = models.CharField(max_length=40)
    startDateTime        = models.DateTimeField(auto_now=False, auto_now_add=False)
    endDateTime          = models.DateTimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return self.name

    def eventDate_Pretty(self):
        return event.date.strftime('%b %e, %Y')

class ScoringEvent(models.Model):
    FORMULA = (
    ('1', 'Formula 1'),
    ('2', 'Formula 2'),
    ('3', 'Formula 3'),
    ('W', 'W Series' ),
    )
    event_ID             = models.ForeignKey(Event, null=True, on_delete=models.SET_NULL)
    name                 = models.CharField(max_length=40)
    formula              = models.CharField(max_length=1, choices=FORMULA)
    eventType            = models.CharField(max_length=1)

    def __str__(self):
        return self.name

    def scoringEventDate_Pretty(self):
        return event.startDTime.strftime('%b %e, %Y')

class Result(models.Model):
    scoringEvent_ID      = models.ForeignKey(ScoringEvent, null=True, on_delete=models.SET_NULL)
    competitor_ID        = models.ForeignKey(Competitor, null=True, on_delete=models.SET_NULL)
    finishPosition       = models.IntegerField()
    startPosition        = models.IntegerField()
    lapOrRaceTime        = models.IntegerField()
    lapsComplete         = models.IntegerField()
    formulaPoints        = models.IntegerField()
    pole                 = models.BooleanField(default=False)
    fastestLap           = models.BooleanField(default=False)
    placesGainedLost     = models.IntegerField()


class AcademyScoringMatrix(models.Model):
    FORMULA = (
    ('1', 'Formula 1'),
    ('2', 'Formula 2'),
    ('3', 'Formula 3'),
    ('W', 'W Series' ),
    )
    pointsType           = models.CharField(max_length=1)
    formula              = models.CharField(max_length=1, choices=FORMULA)
    role                 = models.CharField(max_length=1)
    multiplier           = models.DecimalField(max_digits=6, decimal_places=2)

class ScoringMatches(models.Model):
    player_ID            = models.ForeignKey(TeamProfile, null=True, on_delete=models.SET_NULL)
    result_ID            = models.ForeignKey(Result, null=True, on_delete=models.SET_NULL)
    points_Type          = models.CharField(max_length=1)
    academyPoints        = models.IntegerField()
