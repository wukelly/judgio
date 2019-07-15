from django.db import models
from django.contrib.auth.models import User

# makes sure to delete users when deleting judges in bulk
class JudgeQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for obj in self:
            obj.user.delete()
        super(JudgeQuerySet, self).delete(*args, **kwargs)

# Add organization and job title atributes to users who are Judges
class Judge(models.Model):
    objects = JudgeQuerySet.as_manager()

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    organization = models.CharField(max_length=50)
    job_title = models.CharField(max_length=50)
    sponsor_judge = models.BooleanField(default=False)
    checked_in = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def name(self):
        return self.first_name + ' ' + self.last_name

    def username(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)

    def __str__(self):
        return self.name()
    
# make migration commands
# python manage.py makemigrations judging
# python manage.py sqlmigrate judging 0001
# python manage.py migrate
