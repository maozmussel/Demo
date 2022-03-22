from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /myworkspace/5/
    path('<int:project_id>/', views.detail, name='detail'),
    path('projects/', views.projects, name='projects'),
]
