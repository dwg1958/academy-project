from django.contrib import admin

# Register your models here.
from .models import Competitor
from .models import Event
from .models import Result
from .models import ScoringEvent
from .models import AcademyScoringMatrix
from .models import CompetitorScore
from .models import TeamProfile
from .models import TeamScore

#Show record details in admin table
#https://www.geeksforgeeks.org/customize-django-admin-interface/
class TeamProfileAdmin(admin.ModelAdmin):
    list_display  = ( 'id','user_ID', 'teamName', 'p1_1','p1_2','dateStarted')#, 'is_active')
    search_fields = ('teamName',)

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

class CompetitorAdmin(admin.ModelAdmin):
    list_display  = ('id','surname', 'firstname', 'formula', 'role', 'value')#, 'is_active')
    search_fields = ('surname', 'firstname', 'formula',)
    list_filter   = ('formula',)

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

class EventAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'date', 'formulas', 'startDateTime', 'endDateTime')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True


class ResultAdmin(admin.ModelAdmin):
    list_display  = ('id','scoringEvent_ID', 'competitor_ID', 'finishPosition', 'startPosition', 'fastestLap')
    search_fields = ('scoringEvent_ID', 'finishPosition',)

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

class ScoringEventAdmin(admin.ModelAdmin):
    list_display = ('id','event_ID', 'name', 'formula',  'eventType', 'startDateTime')
    list_filter   = ('formula',)

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

class CompetitorScoreAdmin(admin.ModelAdmin):
    list_display  = ( 'id','result_ID', 'scoringevent_ID', 'pointsType', 't1_score', 't2_score')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True


class AcademyScoringMatrixAdmin(admin.ModelAdmin):
    list_display = ('id','formula', 'teamPosition')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

class TeamScoreAdmin(admin.ModelAdmin):
    list_display = ('id','team_ID', 'cscore_ID', 'pointsType', 'teamPosition','academyPoints')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

############################################################
# Add active/inactive flags in table list to change record field 'is_active'
#    def make_active(modeladmin, request, queryset):
#        queryset.update(is_active = 1)
#        messages.success(request, "Selected Record(s) Marked as Active Successfully !!")
#
#    def make_inactive(modeladmin, request, queryset):
#        queryset.update(is_active = 0)
#        messages.success(request, "Selected Record(s) Marked as Inactive Successfully !!")
#
#    admin.site.add_action(make_active, "Make Active")
#    admin.site.add_action(make_inactive, "Make Inactive")
##############################################################

# Tell admin site to show it for editing
admin.site.register(Competitor, CompetitorAdmin)
admin.site.register(TeamProfile, TeamProfileAdmin)
admin.site.register(CompetitorScore, CompetitorScoreAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(ScoringEvent, ScoringEventAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(AcademyScoringMatrix, AcademyScoringMatrixAdmin)
admin.site.register(TeamScore, TeamScoreAdmin)
