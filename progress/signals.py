from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import LessonProgress, Notification

@receiver(post_save, sender=LessonProgress)
def send_lesson_completion_notification(sender, instance, created, **kwargs):
    if created and instance.is_completed:
        Notification.objects.create(
            user=instance.user,
            message=f"Congratulations! You completed the lesson: {instance.lesson.title}"
        )