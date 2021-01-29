from django.db import models

# Create your models here.
class Competitors(models.Model):
    mugshot              = models.ImageField(upload_to='mugshots/')
    surname              = models.CharField(max_length=20)
    firstname            = models.CharField(max_length=20)
    role                 = models.CharField(max_length=1)
    formula              = models.CharField(max_length=1)
    team                 = models.CharField(max_length=20)
    value                = models.IntegerField()
    nationality          = models.CharField(max_length=20)
    birthdate            = models.DateField(auto_now=False, auto_now_add=False)
    wins                 = models.IntegerField()
    poles                = models.IntegerField()
    championships        = models.IntegerField()
    pointsThisSeason     = models.IntegerField()
    winsThisSeason       = models.IntegerField()
    polesThisSeason      = models.IntegerField()
    gainLossThisseason   = models.IntegerField()
    webLink              = models.CharField(max_length=30)
    instaHandle          = models.CharField(max_length=30)
    twitterHandle        = models.CharField(max_length=30)


    class Meta:
        # Add verbose name
        verbose_name = 'Driver or Manager'
