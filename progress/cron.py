from django_cron import CronJobBase, Schedule
from .models import LessonProgress, Notification

class ReminderCronJob(CronJobBase):
    RUN_EVERY_MINS = 1440  # 24 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'progress.reminder_cron_job'

    def do(self):
        # Notify users about incomplete lessons
        incomplete_lessons = LessonProgress.objects.filter(is_completed=False)
        for lesson in incomplete_lessons:
            Notification.objects.create(
                user=lesson.user,
                message=f"Reminder: Complete your lesson: {lesson.lesson.title}"
            )