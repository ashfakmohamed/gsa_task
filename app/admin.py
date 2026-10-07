from django.contrib import admin

from .models import Profile, Task


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "mobile_number")
    search_fields = ("user__username", "user__email", "mobile_number")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "date", "time", "status")
    list_filter = ("status", "date")
    search_fields = ("name", "owner__username", "assigned_to")
