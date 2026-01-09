from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "role", "status", "progress", "points", "due_date", "updated_at")
    list_filter = ("status", "role", "owner")
    search_fields = ("title", "owner__username", "role")
