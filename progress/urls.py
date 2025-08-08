from django.urls import path
from .views import progress_report_view,leaderboard_view,notification_view,submit_quiz, quiz_attempts_view,notify_user,user_progress_chart,recommend_materials,personalized_recommendations

urlpatterns = [
    path('report/', progress_report_view, name='progress-report'),
    path('leaderboard/', leaderboard_view, name='leaderboard'),
    path('notifications/', notification_view, name='notification'),
     path('quiz/<int:quiz_id>/submit/', submit_quiz, name='submit_quiz'),
    path('quiz/<int:quiz_id>/attempts/', quiz_attempts_view, name='quiz_attempts'),
    path('dashboard/', user_progress_chart, name='user_dashboard'),
    path('recommendations/',personalized_recommendations,name='recommend_materials'),
]


