from django.urls import path
from . import views

urlpatterns = [
    path('exams/', views.exam_list, name='exam_list'),
    path('exams/<int:exam_id>/take/', views.take_exam, name='take_exam'),
    path('exams/submitted/<int:student_exam_id>/', views.exam_submitted, name='exam_submitted'),
    path('exams/<int:student_exam_id>/grade/', views.grade_exam, name='grade_exam'),
    path('exams/graded/<int:student_exam_id>/', views.exam_graded, name='exam_graded'),
    path('exams/submitted/', views.submitted_exams, name='submitted_exams'),
    path('exams/<int:exam_id>/leaderboard/', views.exam_leaderboard, name='exam_leaderboard'),
    path('exams/<int:exam_id>/students/', views.exam_students_list, name='exam_students_list'),
     path('exams/<int:exam_id>/send_file/<int:student_id>/', views.send_exam_file, name='send_exam_file'),
     path('exams/<int:exam_id>/received_files/', views.exam_received_files, name='exam_received_files'),
      path('submitted_exams/', views.submitted_exam_list, name='submitted_exam_list'),
       path('submissions/', views.submissions, name='submissions'),
       path('exam/submitted2/', views.exam_submitted_confirmation, name='exam_submitted_confirmation')
]
