from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=30, null=True)
    prev_choice = models.CharField(max_length=30, null=True)
    next_choice = models.CharField(max_length=30, null=True)
    chat_id = models.CharField(max_length=30, null=True)