from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import StudentRegistrationForm, LoginForm
from .models import UserProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"✅ Welcome, {user.first_name}! Your account has been created.")
            return redirect('home')
        else:
            messages.error(request, "❌ Please correct the errors below.")
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        # Allow login by email
        username_input = request.POST.get('username', '')

        if '@' in username_input:
            try:
                user_obj = User.objects.filter(email=username_input).first()
                request.POST = request.POST.copy()
                request.POST['username'] = user_obj.username
                form = LoginForm(request, data=request.POST)
            except User.DoesNotExist:
                pass
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"👋 Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "❌ Invalid credentials. Please try again.")
    else:
        form = LoginForm(request)
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "👋 You have been logged out.")
    return redirect('login')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(
        user=request.user,
        defaults={'role': 'student'}
    )
    # Count this user's appointments
    from appointments.models import Appointment
    my_appointments = Appointment.objects.filter(
        email=request.user.email
    ).order_by('-date')
    return render(request, 'accounts/profile.html', {
        'profile': profile,
        'my_appointments': my_appointments,
    })