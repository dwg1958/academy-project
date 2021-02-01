from django.db import models

# Create your models here.
class Competitor(models.Model):
    mugshot              = models.ImageField(upload_to='mugshots/')
    surname              = models.CharField(max_length=20)
    firstname            = models.CharField(max_length=20)
    raceNumber           = models.IntegerField(default=0)
    role                 = models.CharField(max_length=1)
    formula              = models.CharField(max_length=1)
    team                 = models.CharField(max_length=20)
    value                = models.DecimalField(max_digits=4, decimal_places=1, default = 0)
    nationality          = models.CharField(max_length=20, blank=True)
    birthdate            = models.DateField(auto_now=False, auto_now_add=False)
    wins                 = models.IntegerField(default = 0)
    poles                = models.IntegerField(default = 0)
    championships        = models.IntegerField(default = 0)
    pointsThisSeason     = models.IntegerField(default = 0)
    winsThisSeason       = models.IntegerField(default = 0)
    polesThisSeason      = models.IntegerField(default = 0)
    gainLossThisseason   = models.IntegerField(default = 0)
    webLink              = models.CharField(max_length=30, blank=True)
    instaHandle          = models.CharField(max_length=30, blank=True)
    twitterHandle        = models.CharField(max_length=30, blank=True)
    short_bio            = models.TextField(default=" ")

    class Meta:
        # Add verbose name
        verbose_name = 'Driver or Manager'

    def birthday_pretty(self):
        return self.birthdate.strftime('%b %e, %Y')

class Event(models.Model):
    name                 = models.CharField(max_length=20)
    date                 = models.DateField(auto_now=False, auto_now_add=False)
    circuit              = models.CharField(max_length=20)
    country              = models.CharField(max_length=20)
    formula              = models.CharField(max_length=1)


class Result(models.Model):
    eventID              = models.IntegerField()
    competitor           = models.IntegerField()
    formula              = models.CharField(max_length=1)
    raceOrQuali          = models.CharField(max_length=1)
    position             = models.IntegerField()
    timeSeconds          = models.DecimalField(max_digits=8, decimal_places=3)
    lapsComplete         = models.IntegerField()
    points               = models.IntegerField()
    pole                 = models.BooleanField(default=False)
    fastestLap           = models.BooleanField(default=False)
    placesGainedLost     = models.IntegerField()
    gridPosition         = models.IntegerField()
