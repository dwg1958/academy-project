from django.db import models
from django.conf import settings
from .formatChecker import ContentTypeRestrictedFileField


# Create your models here.

class Profile(models.Model):
    user            = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    photo           = ContentTypeRestrictedFileField(upload_to='account/mugshots/', default="siteimages/blankUser.png")
    opt_in_to_email = models.BooleanField(default=True)

    def __str__(self):
        return f'Profile for user {self.user.username}'

    class Meta:
        # Add verbose name
        verbose_name = 'Player Profile'
        ordering = ('-user',)
