from django.contrib import admin

from .models import User, Role, Project

admin.site.register(User)
admin.site.register(Role)
admin.site.register(Project)
