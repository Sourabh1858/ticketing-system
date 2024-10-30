from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Activity(models.Model):
    class meta:
        verbose_name_plural = 'Activities'
    class Type(models.TextChoices):
        LOGIN = 'LOGIN'
        LOGOUT = 'LOGOUT'
        CREATE = 'CREATE'
        UPDATE = 'UPDATE'
        DELETE = 'DELETE'
    class Level(models.TextChoices):
        INFO = 'INFO'
        WARNING = 'WARNING'
        ERROR = 'ERROR'
        DEBUG = 'DEBUG'
    user = models.CharField(max_length=16, default='SYSTEM')
    action = models.CharField(max_length=128, choices=Type.choices)
    level = models.CharField(max_length=11, choices=Level.choices, default=Level.INFO)
    log = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

# class NewUser(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     projects = models.CharField(max_length=256)  # Adjust the length as needed

#     def __str__(self):
#         return f"{self.user.username} - {self.projects}"
class NewUser(models.Model):
    PROJECT_OPTIONS = (
        ('AMD BANK', 'AMD BANK'),
        ('EARNING WEALTH SYSTEM', 'EARNING WEALTH SYSTEM'),
        ('AI & ML', 'AI & ML'),
        ('MEET FINANCE', 'MEET FINANCE'),
        ('AJIT MULTI TASK', 'AJIT MULTI TASK'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.CharField(max_length=1024 ,choices=PROJECT_OPTIONS,default="")  # Store project name directly

    def __str__(self):
        return f"{self.user.username} - {self.project}"