from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'student_id', 'contact', 'created_at']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email', 'student_id']
    list_editable = ['role']