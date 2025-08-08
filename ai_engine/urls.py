from django.urls import path
from .views import educational_content_list,dataset_list,kcse_papers
from . import views

urlpatterns = [
    path('educational-content/', educational_content_list, name='educational_content_list'),
     path('datasets/', dataset_list, name='dataset_list'),
     path('kcse-past-papers/', kcse_papers, name='kcse_past_papers'),
      path('subject-notes/', views.subject_notes, name='subject_notes'),
    path('shared-resources/', views.shared_resources, name='shared_resources'),
    path('submit-note/', views.submit_note, name='submit_note'),
    path('submit-resource/', views.submit_resource, name='submit_resource'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('approve-resource/<int:resource_id>/', views.approve_resource, name='approve_resource'),
    path('notifications/', views.user_notifications, name='notifications2'),
        
]