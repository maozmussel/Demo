from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /myworkspace/5/
    path('<int:project_id>/', views.detail, name='detail'),
    # ex: /myworkspace/projects/
    path('projects/', views.projects, name='projects'),
    # ex: /myworkspace/project_upload/
    path('project_upload/', views.upload_project_form, name='project_upload'),
    # ex: /myworkspace/upload_projects_from_csv/
    path('upload_projects_from_csv/', views.upload_projects_from_csv, name='upload_projects_from_csv'),
]
