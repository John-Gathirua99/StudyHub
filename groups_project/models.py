from django.db import models
from django.contrib.auth.models import User

class Group(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(User, related_name="groups")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="projects")
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to="projects/")
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title