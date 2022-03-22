from django.db import models

class Project(models.Model):
    project_name = models.CharField(max_length=50)
    created_date = models.DateTimeField('date created')
    survey_id = models.IntegerField(default=0)
    survey_url = models.CharField(max_length=200, null=True)
    survey_type = models.CharField(max_length=30, default='General')

    def __str__(self):
        return self.project_name
