from django.urls import path

from . import views
from accounts import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('faq/', views.faq, name='faq'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.appointments_list, name='appointments_list'),
    path('appointments/<int:pk>/edit/', views.edit_appointment, name='edit_appointment'),
    path('appointments/<int:pk>/delete/', views.delete_appointment, name='delete_appointment'),
    path('appointments/<int:pk>/status/', views.update_status, name='update_status'),
    path('profile/',views.profile_view, name='profile'),
     path('logout/', auth_views.logout_view, name='logout'),
     path('login/', auth_views.login_view, name='login'),
     path('register/', auth_views.register_view, name='register'),
  
]
