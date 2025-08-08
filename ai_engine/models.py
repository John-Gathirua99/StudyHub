from django.db import models
from django.contrib.auth.models import User

class EducationalContent(models.Model):
    """Model to store educational content for students."""
    CONTENT_TYPES = [
        ('video', 'Video'),
        ('photo', 'Photo'),
        ('file', 'File'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    content_type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    file = models.FileField(upload_to='educational_content/files/', null=True, blank=True)
    photo = models.ImageField(upload_to='educational_content/photos/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    


class Dataset(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='datasets/')
    source_url = models.URLField(blank=True, null=True)


from django.db import models

class KcsePastPaper(models.Model):
    subject = models.CharField(max_length=100)
    year = models.IntegerField()
    paper_type = models.CharField(max_length=50, choices=[
        ('Paper 1', 'Paper 1'),
        ('Paper 2', 'Paper 2'),
        ('Paper 3', 'Paper 3'),
    ])
    file = models.FileField(upload_to='kcse_pastpapers/')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.subject} {self.year} {self.paper_type}"
    


class SubjectNote(models.Model):
    subject = models.CharField(max_length=100)
    topic = models.CharField(max_length=255)
    file = models.FileField(upload_to='subject_notes/')
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.subject} - {self.topic}"

class SharedResource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='shared_resources/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)  # Only visible if approved by a teacher

    def __str__(self):
        return self.title

class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE,related_name="ai_engine_notifications")
    message = models.CharField(max_length=255)
    link = models.URLField(blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_teacher = models.BooleanField(default=False)

#Chatbot


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
