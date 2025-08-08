from django.db import models
from django.contrib.auth.models import User
from users.models import Profile

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Exam(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    max_marks = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.exam.title}: {self.text[:50]}"

class StudentExam(models.Model):
    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    graded = models.BooleanField(default=False)
    submitted=models.BooleanField(default=False)
    total_marks = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.student} - {self.exam}"

class StudentAnswer(models.Model):
    student_exam = models.ForeignKey(StudentExam, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    marks_awarded = models.PositiveIntegerField(null=True, blank=True)
    checked_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    checked_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Answer by {self.student_exam.student} for '{self.question.text[:30]}'"
    



class ExamFileMessage(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, related_name='sent_files', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, related_name='received_files', on_delete=models.CASCADE)
    file = models.FileField(upload_to='exam_files/%Y/%m/%d/')
    message = models.TextField(blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver} ({self.exam})"