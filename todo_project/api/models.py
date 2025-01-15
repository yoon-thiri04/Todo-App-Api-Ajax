from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Task(models.Model):
    title=models.CharField(max_length=50)
    completed=models.BooleanField(default=False,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title
