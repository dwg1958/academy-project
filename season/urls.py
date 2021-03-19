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
    path( 'teamnamepicker',    views.teamnamepicker        , name = "teamnamepicker"),
    path( 'addcompetitors',    views.addcompetitors        , name = "addcompetitors"),
    path( 'addevents',         views.addevents             , name = "addevents"),
    path( 'scoreevents',       views.scoreevents           , name = "scoreevents"),
    path( 'addresults',        views.addresults            , name = "addresults"),
    path( 'showevents',        views.showevents            , name = "showevents"),
    path( 'showscoringevents', views.showscoringevents     , name = "showscoringevents"),
    path( 'showresults',       views.showresults           , name = "showresults"),
    path( 'leagueposition',    views.leagueposition        , name = "leagueposition"),
    path( 'rebuildleagues',    views.rebuildleagues        , name = "rebuildleagues"),
    path( 'scoring',           views.scoring               , name = "scoring"),
    path( 'test',              views.test                  , name = "test"),

#    path( '<int:blog_id>/', views.oneblog, name = "oneblog"),

]
