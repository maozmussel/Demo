"""Demo App URL Configuration

"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('myworkspace/', include('myworkspace.urls')),
    path('admin/', admin.site.urls),
]
