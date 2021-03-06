from django.db import models

class Project(models.Model):
    project_name = models.CharField(max_length=120)
    created_date = models.DateTimeField('date created')
    survey_id = models.IntegerField(default=0)
    survey_url = models.CharField(max_length=200, null=True)
    survey_type = models.CharField(max_length=30, default='General')
    team = models.CharField(max_length=30, default=0)
    survey_status = models.CharField(max_length=30, default='')
    project_status = models.CharField(max_length=10, default='Open')

    def __str__(self):
        return self.project_name

class Project_statuses(models.Model):
    status_id = models.IntegerField(primary_key=True)
    status_name = models.CharField(max_length=10)

ps = Project_statuses(1, 'Open')
ps.save()
ps = Project_statuses(2, 'Closed')
ps.save()

class Survey_responses_aggregate(models.Model):
    survey_id = models.IntegerField(default=0)
    question_id = models.IntegerField(default=0)
    option_value = models.CharField(max_length=120)
    option_count = models.IntegerField(default=0)
