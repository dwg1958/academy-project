"""
This is the urls.py for the season section of the Academy project ONLY
"""

from django.urls import path

from .import views   # not blog.views because we're in it


urlpatterns = [

    path( '', views.tables, name = "tables"),
    path( 'tables', views.tables, name = "tables"),
    path('tables/<formula>/', views.tableformula, name = "tableformula"),
    path( 'maketeam', views.maketeam, name = "maketeam"),
    path( 'teampicker', views.teampicker, name = "teampicker"),
#    path( '<int:blog_id>/', views.oneblog, name = "oneblog"),

]
