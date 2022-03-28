from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # main page
    path('', views.index, name='index'),
    # project list
    path('projects/', views.projects, name='projects'),
    # project details, ex: /myworkspace/projects/5/
    path('projects/<int:project_id>/', views.project_details, name='project_details'),

    # upload projects from csv form
    path('project_upload/', views.upload_project_form, name='project_upload'),
    # upload projects from csv action 
    path('upload_projects_from_csv/', views.upload_projects_from_csv, name='upload_projects_from_csv'),

    # fetch Alchemer data into csv file - form
    path('fetch_data/', views.fetch_data_form, name='fetch_data'),
    # fetch Alchemer data into csv file - action
    path('fetch_alchemer_data/', views.fetch_alchemer_data, name='fetch_alchemer_data'),

    # highcharts
    path('highcharts/', views.generate_highcharts, name='generate_highcharts'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
