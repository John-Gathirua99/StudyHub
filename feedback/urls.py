from django.urls import path
from . import views

urlpatterns = [
    path('chat/<str:room_name>/', views.chat_view, name='chat'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('timetable/', views.timetable_view, name='timetable'),
]