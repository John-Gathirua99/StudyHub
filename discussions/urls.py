from django.urls import path
from . import views

urlpatterns = [
    path('', views.thread_list, name='thread_list'),
    path('thread/<int:thread_id>/', views.thread_detail, name='thread_detail'),
    path('inbox/', views.inbox, name='inbox'),
    # path('messages/',views.user_messages,name='user_messages'),
    path('thread/<int:other_user_id>/', views.user_thread, name='user_thread'),
     path('reply/<int:message_id>/', views.reply_message_view, name='reply_message'),
    path('send-message/', views.send_private_message, name='send_private_message'),
]