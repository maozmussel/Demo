from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Project
import csv
import datetime


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

def is_member_in_group(user, group):
    return user.groups.filter(name=group).exists()

@login_required
def upload_project_form(request):
    if (is_member_in_group(request.user, 'Admin Group')):
        return render(request, 'myworkspace/upload_csv.tmpl')
    else:
        return HttpResponse("You do not have premissions for this operation")

def upload_projects_from_csv(request):
    file_name=request.POST['fname']
    try:
        csv_file = open(file_name)
    except (FileNotFoundError, IOError):
        return HttpResponse("Wrong file or file path.")
    with csv_file:
        csvfile = csv.reader(csv_file, delimiter=',')
        header = next(csvfile)
        row_values = []
        try:
            for row in csvfile:
                #row_values.append(row)
                obj, created = Project.objects.update_or_create(
                    project_name=row[0],
                    created_date=datetime.datetime.strptime(row[1].strip(), '%Y-%m-%d %H:%M:%S').date(),
                    survey_id=row[2],
                    survey_url=row[3],
                    survey_type=row[4],
                )
        except:
            return HttpResponse("Problem on uploading projects, please check the file format.")
        finally:
            csv_file.close()
    return HttpResponse("Upload completed succesfully.")
