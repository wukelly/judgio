from django.db import models
from django.contrib.auth.models import User

class Judge(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
