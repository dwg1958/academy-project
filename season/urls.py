"""
This is the urls.py for the season section of the Academy project ONLY
"""

from django.urls import path

from .import views   # not blog.views because we're in it


urlpatterns = [

    path( '',                  views.tables                , name = "tables"),
    path( 'tables',            views.tables                , name = "tables"),
    path('tables/<formula>/',  views.tableformula          , name = "tableformula"),
    path( 'teamview',          views.teamview              , name = "teamview"),
    path( 'teampicker',        views.teampicker            , name = "teampicker"),
    path( 'addcompetitors',    views.addcompetitors        , name = "addcompetitors"),
    path( 'addevents',         views.addevents             , name = "addevents"),
    path( 'addscoringevents',  views.addscoringevents      , name = "addscoringevents"),
    path( 'addresults',        views.addresults            , name = "addresults"),
    path( 'showevents',        views.showevents            , name = "showevents"),
    path( 'showscoringevents', views.showscoringevents     , name = "showscoringevents"),
    path( 'showresults',       views.showresults           , name = "showresults"),

#    path( '<int:blog_id>/', views.oneblog, name = "oneblog"),

]
