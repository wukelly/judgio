from django.db import models
from django.contrib.auth.models import User

# Add organization and job title atributes to users who are Judges
class Judge(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    organization = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    sponsor_judge = models.BooleanField(default=False)
    checked_in = models.BooleanField(default=False)

    def name(self):
        return self.first_name + ' ' + self.last_name

    def email(self):
        return self.user.email

# make migration commands
# python manage.py makemigrations judging
# python manage.py sqlmigrate judging 0001
# python manage.py migrate
