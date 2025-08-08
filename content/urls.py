from django.urls import path
from .views import lesson_list_view, lesson_detail_view, quiz_view,homepage

urlpatterns = [
    path('',homepage,name='home'),
    path('lessons/', lesson_list_view, name='lesson-list'),
    path('lessons/<int:lesson_id>/', lesson_detail_view, name='lesson-detail'),
    path('lessons/<int:lesson_id>/quiz/', quiz_view, name='lesson-quiz'),
]