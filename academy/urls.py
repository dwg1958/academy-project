
########## URLS.PY ##########

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('season/', include('season.urls')),
    path('account/', include('account.urls')),
    path('', views.homepage, name='home'),
    path('about/', views.aboutpage, name='about'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
