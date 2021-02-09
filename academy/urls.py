
########## URLS.PY ##########

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path( 'login/', views.login, name = "login"),
    path( 'register/', views.register, name = "register"),
    path( 'login/', views.login, name = "login"),
    path( 'logout/', views.logout, name = "logout"),
    path('', views.homepage, name='home'),
    path('about/', views.aboutpage, name='about'),
    path('season/', include('season.urls')),   # send ANYTHING blog to a new urls.py program
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
