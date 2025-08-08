from django.contrib.auth.models import User
from django.db import models

class DiscussionThread(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='threads')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ThreadMessage(models.Model):
    thread = models.ForeignKey(DiscussionThread, on_delete=models.CASCADE, related_name='messages')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    media = models.FileField(upload_to='thread_media/', blank=True, null=True)  # For images or videos
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message by {self.author} in {self.thread}"


class PrivateMessage(models.Model):
    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='private_messages_sent'  # Unique related_name for sender
    )
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='private_messages_received'  # Unique related_name for recipient
    )
    content = models.TextField()
    media = models.FileField(upload_to='private_media/', blank=True, null=True)  # For images or videos
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"