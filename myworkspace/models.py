from django.db import models

class Role(models.Model):
    role_id = models.IntegerField(primary_key=True)
    role_name = models.CharField(max_length=20)

    def __str__(self):
        return self.role_name

class User(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=20)
    full_name = models.CharField(max_length=50)
    role = models.ForeignKey(Role, on_delete=models.PROTECT)

    def __str__(self):
        return self.username

class Project(models.Model):
    project_id = models.IntegerField(default=0)
    project_name = models.CharField(max_length=50)
    created_date = models.DateTimeField('date created')
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    survey_id = models.IntegerField(default=0)
    survey_url = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.project_name
