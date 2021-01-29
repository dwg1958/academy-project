from django.contrib import admin

# Register your models here.
from .models import Competitors

#Show record details in admin table
#https://www.geeksforgeeks.org/customize-django-admin-interface/
class CompetitorAdmin(admin.ModelAdmin):
    list_display = ('surname', 'firstname', 'formula', 'role')#, 'is_active')

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
admin.site.register(Competitors, CompetitorAdmin)
