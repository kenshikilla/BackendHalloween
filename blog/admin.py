from django.contrib import admin
from .models import Ticket

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('name', 'priority', 'created_date')
    list_filter = ('priority', 'created_date')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_date'

admin.site.register(Ticket, ProblemAdmin)
