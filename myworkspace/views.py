import logging
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
import pandas as pd
from pandas_highcharts.core import serialize
from .models import Project
from .constant import constant
from .fetch_alchemer_to_csv import *
from .upload_data_from_csv import *
from .highcharts_create import *

# define logging
logging.basicConfig(level=logging.DEBUG,
    format='%(asctime)s %(levelname)s %(message)s',
    filename=f"{constant.OUTPUT_DIR}/myworkspace.log",
    filemode='w')

@login_required
def index(request):
    """app main page"""
    return render(request, 'myworkspace/index.html')

@login_required
def projects(request):
    """Display list of projects"""
    return render(request, 'myworkspace/project.tmpl', {'obj': Project.objects.all()})

@login_required
def project_details(request, project_id):
    """Display project details based on the project id key.

       Display content in page if the given is exists, 404 otherwise
    """
    try:
        project = Project.objects.get(pk=project_id)
        project.created_date = f"{project.created_date:%d-%m-%Y}"
    except Project.DoesNotExist:
        raise Http404("Project does not exist")
    return render(request, 'myworkspace/project_details.tmpl', {'project': project})


def is_member_in_group(user, group):
    """Check if a user belongs to a gorup, return true if exist.

       user - the reequest user identifier
       group - the group name
    """
    return user.groups.filter(name=group).exists()

@login_required
def fetch_data_form(request):
    """Display form to fetch data from Alchemer"""
    if (is_member_in_group(request.user, constant.ADMIN_GROUP_NAME)):
        return render(request, 'myworkspace/fetch_data.tmpl')
    else:
        return HttpResponse("You do not have premissions for this operation.")

@login_required
def fetch_alchemer_data(request):
    """Fetch data from Alchemer using REST API"""
    # get form parameters - the output file name and the date range
    file_name = request.POST['fname']
    from_date = request.POST['fromdate']
    to_date = request.POST['todate']
    res = fetch_survey_data_into_csv(file_name, from_date, to_date)
    if (res == "Success"):
        return HttpResponse("Oprtation completed succesfully.")
    else:
        return HttpResponse(f"Oprtation failed: {res}.")


@login_required
def upload_project_form(request):
    """Display form to upload project data from csv into the database """
    if (is_member_in_group(request.user, constant.ADMIN_GROUP_NAME)):
        return render(request, 'myworkspace/upload_csv.tmpl')
    else:
        return HttpResponse("You do not have premissions for this operation.")

def upload_projects_from_csv(request):
    """Upload project data from csv into the database """
    res = do_upload_projects_from_csv(request)
    if (res == "Success"):
        return HttpResponse("Oprtation completed succesfully.")
    else:
        return HttpResponse(f"Oprtation failed: {res}.")

@login_required
def define_highcharts(request):
    return render(request, 'myworkspace/highcharts.html')

def generate_highcharts(request):
    sid = request.POST.get('Survey', 0)
    chart_type = request.POST.get('Type', "pie")
    charts = generate_highcharts_plot(sid, chart_type)
    return render(request, 'myworkspace/highcharts.tmpl', {'charts': charts, 'Survey': sid, 'Type': chart_type})
