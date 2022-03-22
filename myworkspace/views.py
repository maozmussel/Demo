from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import render
#from django.db import models
from .models import Project
from django.contrib.auth.decorators import login_required

def index(request):
    latest_project_list = Project.objects.order_by('-project_name')[:5]
    template = loader.get_template('myworkspace/index.html')
    context = {
        'latest_project_list': latest_project_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except Project.DoesNotExist:
        raise Http404("Project does not exist")
    return render(request, 'myworkspace/detail.html', {'project': project})

@login_required
def projects(request):
    return render(request, 'myworkspace/project.tmpl', {'obj': Project.objects.all()})
