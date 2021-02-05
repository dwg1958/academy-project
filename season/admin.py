from django.contrib import admin

# Register your models here.
from .models import Competitor
from .models import Event
from .models import Result
from .models import ScoringEvent
from .models import AcademyScoringMatrix
from .models import ScoringMatches

#Show record details in admin table
#https://www.geeksforgeeks.org/customize-django-admin-interface/
class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('id','surname', 'firstname', 'formula', 'role')#, 'is_active')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

class EventAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'date', 'formulas')#, 'is_active')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

class ResultAdmin(admin.ModelAdmin):
    list_display = ('id','scoringEvent_ID', 'competitor_ID', 'eventType', 'finishPosition')#, 'is_active')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

class ScoringEventAdmin(admin.ModelAdmin):
    list_display = ('id','event_ID', 'name', 'formula', 'eventType', 'startDateTime', 'endDateTime')#, 'is_active')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

class AcademyScoringMatrixAdmin(admin.ModelAdmin):
    list_display = ('id','pointsType', 'formula', 'role', 'multiplier')#, 'is_active')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

class ScoringMatchesAdmin(admin.ModelAdmin):
    list_display = ('id','player_ID', 'result_ID', 'points_Type', 'academyPoints')#, 'is_active')

    def active(self, obj):
        return obj.is_active == 1

    active.boolean = True

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

# Tell admin site to show it for editing
admin.site.register(Competitor, CompetitorAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Result, ResultAdmin)
admin.site.register(ScoringEvent, ScoringEventAdmin)
admin.site.register(AcademyScoringMatrix, AcademyScoringMatrixAdmin)
admin.site.register(ScoringMatches, ScoringMatchesAdmin)
