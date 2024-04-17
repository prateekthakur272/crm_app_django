from django.contrib import admin
from django.contrib.admin import ModelAdmin
from .models import Record

# admin.site.register(Record)
@admin.register(Record)
class AdminRecord(ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'city']