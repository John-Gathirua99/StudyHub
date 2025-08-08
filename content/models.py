from django.db import models

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    difficulty_level = models.CharField(max_length=50)
    topic = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Quiz(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='quizzes')
    question = models.TextField()
    option_a = models.CharField(max_length=255,default='Study of chemicals')
    option_b = models.CharField(max_length=255,default='Study of chemicals')
    option_c = models.CharField(max_length=255,default='Study of chemicals')
    option_d = models.CharField(max_length=255,default='Study of chemicals')
    correct_option = models.CharField(max_length=1, choices=[
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ],default='A')

    def __str__(self):
        return f"Quiz for Lesson: {self.lesson.title}"




