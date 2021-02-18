from django.db import models
from django.conf import settings


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    date_of_birth = models.DateField(blank=True, null=True)
    #photo = models.ImageField(upload_to='users/%Y/%m/%d/',blank=True)
    photo = models.ImageField(upload_to='account/mugshots/', default="siteimages/blankUser.png")

    def __str__(self):
        return f'Profile for user {self.user.username}'

    class Meta:
        # Add verbose name
        verbose_name = 'Player Profile'
        ordering = ('-user',)
