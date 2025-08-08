from django.contrib import admin
from .models import Teacher, Student, Exam, Question, StudentExam, StudentAnswer

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(StudentExam)
admin.site.register(StudentAnswer)