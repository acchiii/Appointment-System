from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from accounts.models import UserProfile

from .models import Appointment
from .forms import AppointmentForm, AppointmentSearchForm
import datetime



def _get_role(user):

    try:
        return user.profile.role
    except Exception:
        return 'student'


def _is_staff_or_admin(user):
    return _get_role(user) in ('staff', 'admin')


def _is_admin(user):
    return _get_role(user) == 'admin'




def home(request):
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


def faq(request):
    return render(request, 'appointments/faq.html')


@login_required
def book_appointment(request):
   
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            messages.success(
                request,
                f'Appointment booked successfully! Reference: APT-{appointment.id:04d}'
            )
            return redirect('appointments_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        initial = {'email': request.user.email}
        full_name = request.user.get_full_name()
        if full_name:
            initial['student_name'] = full_name
        try:
            profile = request.user.profile
            if profile.student_id:
                initial['student_id'] = profile.student_id
            if profile.contact:
                initial['contact'] = profile.contact
        except Exception:
            pass
        form = AppointmentForm(initial=initial)

    return render(request, 'appointments/book.html', {'form': form})


@login_required
def appointments_list(request):
  
    role = _get_role(request.user)
    search_form = AppointmentSearchForm(request.GET or None)

    if role in ('staff', 'admin'):
        appointments = Appointment.objects.all()
    else:
        appointments = Appointment.objects.filter(email=request.user.email)

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
        'is_staff_or_admin': _is_staff_or_admin(request.user),
        'is_admin': _is_admin(request.user),
        'role': role,
    }
    return render(request, 'appointments/appointments_list.html', context)


@login_required
def edit_appointment(request, pk):
   
    appointment = get_object_or_404(Appointment, pk=pk)
    role = _get_role(request.user)

    if role == 'student':
        if appointment.email != request.user.email:
            messages.error(request, "You don't have permission to edit this appointment.")
            return redirect('appointments_list')
        if appointment.status != 'pending':
            messages.error(request, "Only pending appointments can be edited.")
            return redirect('appointments_list')

    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, f'Appointment APT-{appointment.id:04d} updated successfully!')
            return redirect('appointments_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = AppointmentForm(instance=appointment)

    return render(request, 'appointments/edit_appointment.html', {
        'form': form,
        'appointment': appointment,
        'is_staff_or_admin': _is_staff_or_admin(request.user),
        'is_admin': _is_admin(request.user),
    })


@login_required
def delete_appointment(request, pk):
   
    appointment = get_object_or_404(Appointment, pk=pk)
    role = _get_role(request.user)

    if role == 'student':
        if appointment.email != request.user.email:
            messages.error(request, "You don't have permission to delete this appointment.")
            return redirect('appointments_list')
        if appointment.status not in ('pending', 'cancelled'):
            messages.error(request, "Only pending appointments can be cancelled.")
            return redirect('appointments_list')

    if request.method == 'POST':
        appt_ref = f'APT-{appointment.id:04d}'
        appointment.delete()
        messages.success(request, f'Appointment {appt_ref} has been deleted.')
        return redirect('appointments_list')

    return render(request, 'appointments/confirm_delete.html', {
        'appointment': appointment,
        'is_staff_or_admin': _is_staff_or_admin(request.user),
    })


@login_required
def update_status(request, pk):
 
    if not _is_staff_or_admin(request.user):
        messages.error(request, "Only staff or admin can update appointment status.")
        return redirect('appointments_list')

    appointment = get_object_or_404(Appointment, pk=pk)
    new_status = request.POST.get('status')
    valid_statuses = ['pending', 'approved', 'done', 'cancelled']

    if request.method == 'POST' and new_status in valid_statuses:
        appointment.status = new_status
        appointment.save()
        messages.success(
            request,
            f'Status updated to "{appointment.get_status_display()}" for APT-{appointment.id:04d}.'
        )

    return redirect('appointments_list')
@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'student'}
    )
    
    from appointments.models import Appointment
    my_appointments = Appointment.objects.filter(
        email=request.user.email
    ).order_by('-date')
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'my_appointments': my_appointments,
    })

def error404(request, error):
    return render('appointments/404.html')
def error500(request):
    return render('appointments/500.html')
