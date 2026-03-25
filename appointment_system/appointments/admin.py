from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'student_name', 'student_id', 'office',
        'date', 'time', 'purpose', 'status', 'created_at'
    ]
    list_filter = ['status', 'office', 'date', 'purpose']
    search_fields = ['student_name', 'student_id', 'email', 'contact']
    list_editable = ['status']
    ordering = ['-date', '-time']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'

    fieldsets = (
        ('Student Information', {
            'fields': ('student_name', 'student_id', 'email', 'contact')
        }),
        ('Appointment Details', {
            'fields': ('office', 'date', 'time', 'purpose', 'notes')
        }),
        ('Status & Metadata', {
            'fields': ('status', 'created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

    actions = ['mark_approved', 'mark_done', 'mark_cancelled']

    def mark_approved(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} appointment(s) marked as Approved.")
    mark_approved.short_description = "Mark selected as Approved"

    def mark_done(self, request, queryset):
        queryset.update(status='done')
        self.message_user(request, f"{queryset.count()} appointment(s) marked as Done.")
    mark_done.short_description = "Mark selected as Done"

    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
        self.message_user(request, f"{queryset.count()} appointment(s) marked as Cancelled.")
    mark_cancelled.short_description = "Mark selected as Cancelled"



admin.site.site_header = "SchoolDesk Admin Panel"
admin.site.site_title = "SchoolDesk"
admin.site.index_title = "Appointment Management System"
