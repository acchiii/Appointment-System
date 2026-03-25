from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    student_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="Student ID")
    contact = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    def is_student(self):
        return self.role == 'student'

    def is_staff_member(self):
        return self.role in ('staff', 'admin')

    def is_admin(self):
        return self.role == 'admin'