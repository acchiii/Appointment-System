# Generated migration for appointments app

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=150, verbose_name='Full Name')),
                ('student_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='Student ID / Reference No.')),
                ('email', models.EmailField(max_length=254, verbose_name='Email Address')),
                ('contact', models.CharField(max_length=20, verbose_name='Contact Number')),
                ('office', models.CharField(
                    choices=[
                        ('registrar', 'Registrar Office'),
                        ('enrollment', 'Enrollment Office'),
                        ('document', 'Document Services'),
                    ],
                    default='registrar',
                    max_length=50,
                    verbose_name='School Office',
                )),
                ('date', models.DateField(verbose_name='Appointment Date')),
                ('time', models.TimeField(verbose_name='Appointment Time')),
                ('purpose', models.CharField(
                    choices=[
                        ('tor_request', 'Transcript of Records (TOR) Request'),
                        ('enrollment', 'Enrollment Inquiry'),
                        ('document_request', 'Document Request'),
                        ('certification', 'Certification / Certificate of Enrollment'),
                        ('good_moral', 'Good Moral Certificate'),
                        ('diploma_request', 'Diploma / Graduation Documents'),
                        ('grade_inquiry', 'Grade / Academic Inquiry'),
                        ('other', 'Other Concern'),
                    ],
                    max_length=50,
                    verbose_name='Purpose / Concern',
                )),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Additional Notes')),
                ('status', models.CharField(
                    choices=[
                        ('pending', 'Pending'),
                        ('approved', 'Approved'),
                        ('done', 'Done'),
                        ('cancelled', 'Cancelled'),
                    ],
                    default='pending',
                    max_length=20,
                    verbose_name='Status',
                )),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Appointment',
                'verbose_name_plural': 'Appointments',
                'ordering': ['-date', '-time'],
            },
        ),
    ]
