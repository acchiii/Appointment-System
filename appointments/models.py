from django.db import models


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ]

    PURPOSE_CHOICES = [
        ('tor_request', 'Transcript of Records (TOR) Request'),
    
        ('document_request', 'Document Request'),
        ('certification', 'Certification / Certificate of Enrollment'),
        ('good_moral', 'Good Moral Certificate'),
        ('diploma_request', 'Diploma / Graduation Documents'),
        ('grade_inquiry', 'Grade / Academic Inquiry'),
        ('other', 'Other Concern'),
    ]

    OFFICE_CHOICES = [
        ('registrar', 'Registrar Office'),
        ('document', 'Document Services'),
    ]

    student_name = models.CharField(max_length=150, verbose_name="Full Name")
    student_id = models.CharField(
        max_length=50, blank=True, null=True,
        verbose_name="Student ID / Reference No."
    )
    email = models.EmailField(verbose_name="Email Address")
    contact = models.CharField(max_length=20, verbose_name="Contact Number")
    office = models.CharField(
        max_length=50, choices=OFFICE_CHOICES,
        default='registrar', verbose_name="School Office"
    )
    date = models.DateField(verbose_name="Appointment Date")
    time = models.TimeField(verbose_name="Appointment Time")
    purpose = models.CharField(
        max_length=50, choices=PURPOSE_CHOICES,
        verbose_name="Purpose / Concern"
    )
    notes = models.TextField(
        blank=True, null=True,
        verbose_name="Additional Notes"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='pending', verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    def __str__(self):
        return f"{self.student_name} — {self.get_purpose_display()} [{self.date}]"

    def get_status_badge_class(self):
        classes = {
            'pending': 'badge-pending',
            'approved': 'badge-approved',
            'done': 'badge-done',
            'cancelled': 'badge-cancelled',
        }
        return classes.get(self.status, 'badge-pending')
