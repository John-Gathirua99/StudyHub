from django.urls import path
from . import views
from django.urls import path
from .views import signup_view, login_view, logout_view, profile_view,SafePasswordResetView
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('signup/', signup_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/<int:user_id>/', profile_view, name='user-profile'),
    path('students/', views.student_list_view, name='student_list'),

    path('password-reset/', 
         SafePasswordResetView.as_view(template_name='users/password_reset.html'), 
         name='password_reset'),

    # Built-in views with your templates
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), 
         name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), 
         name='password_reset_confirm'),

    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'), 
         name='password_reset_complete'),

     path('request-otp/', views.request_otp, name='request_otp'),
     path('verify-otp/<int:user_id>/', views.verify_otp, name='verify_otp')
]
