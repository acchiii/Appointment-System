from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Appointment
from .forms import AppointmentForm, AppointmentSearchForm
import datetime


def home(request):
    """Landing / home page with system overview."""
    today = datetime.date.today()
    total = Appointment.objects.count()
    today_count = Appointment.objects.filter(date=today).count()
    pending_count = Appointment.objects.filter(status='pending').count()
    approved_count = Appointment.objects.filter(status='approved').count()
    recent = Appointment.objects.order_by('-created_at')[:5]

    context = {
        'total': total,
        'today_count': today_count,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'recent': recent,
    }
    return render(request, 'appointments/home.html', context)


def book_appointment(request):
    """Create a new appointment."""
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            messages.success(
                request,
                f'✅ Appointment booked successfully! Reference: APT-{appointment.id:04d}'
            )
            return redirect('appointments_list')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/book.html', {'form': form})


def appointments_list(request):
    """View all appointments with search and filter."""
    search_form = AppointmentSearchForm(request.GET or None)
    appointments = Appointment.objects.all()

    if search_form.is_valid():
        search_query = search_form.cleaned_data.get('search')
        office_filter = search_form.cleaned_data.get('office')
        status_filter = search_form.cleaned_data.get('status')
        date_filter = search_form.cleaned_data.get('date_filter')

        if search_query:
            appointments = appointments.filter(
                Q(student_name__icontains=search_query) |
                Q(student_id__icontains=search_query) |
                Q(purpose__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        if office_filter:
            appointments = appointments.filter(office=office_filter)
        if status_filter:
            appointments = appointments.filter(status=status_filter)
        if date_filter:
            appointments = appointments.filter(date=date_filter)

    context = {
        'appointments': appointments,
        'search_form': search_form,
        'total_shown': appointments.count(),
    }
    return render(request, 'appointments/appointments_list.html', context)


def edit_appointment(request, pk):
    """Edit an existing appointment."""
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f'✅ Appointment APT-{appointment.id:04d} updated successfully!'
            )
            return redirect('appointments_list')
        else:
            messages.error(request, '❌ Please correct the errors below.')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'appointments/edit_appointment.html', {
        'form': form,
        'appointment': appointment,
    })


def delete_appointment(request, pk):
    """Delete appointment with confirmation."""
    appointment = get_object_or_404(Appointment, pk=pk)

    if request.method == 'POST':
        appt_ref = f'APT-{appointment.id:04d}'
        appointment.delete()
        messages.success(request, f'🗑️ Appointment {appt_ref} has been deleted.')
        return redirect('appointments_list')

    return render(request, 'appointments/confirm_delete.html', {
        'appointment': appointment,
    })


def update_status(request, pk):
    """AJAX-friendly status update for admin use."""
    appointment = get_object_or_404(Appointment, pk=pk)
    new_status = request.POST.get('status')
    valid_statuses = ['pending', 'approved', 'done', 'cancelled']

    if request.method == 'POST' and new_status in valid_statuses:
        appointment.status = new_status
        appointment.save()
        messages.success(
            request,
            f'✅ Status updated to "{appointment.get_status_display()}" for APT-{appointment.id:04d}.'
        )

    return redirect('appointments_list')
