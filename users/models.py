from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone
import datetime

    
class Profile(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='users_profile',null=True)
    full_name = models.CharField(max_length=150, blank=True)
    grade = models.CharField(max_length=50, blank=True)
    school = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    dob = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='teacher')

    def __str__(self):
        return self.user.username

    
    



class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()

    def is_valid(self):
        return timezone.now() <= self.valid_until
