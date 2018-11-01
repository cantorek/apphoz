from datetime import datetime
from pprint import pprint

from django.contrib.auth import get_user_model
from django.db import models

from .utils import template_parameter

import requests

import json

# Create your models here.

class Language(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    version = models.CharField(max_length=36)

    class Meta:
        unique_together = ('name', 'version')

    def __str__(self):
        return '{0}:{1}'.format(self.name, self.version)


class Framework(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    version = models.CharField(max_length=36)

    class Meta:
        unique_together = ('name', 'version')

    def __str__(self):
        return '{0}:{1}'.format(self.name, self.version)



class App(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=False)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    template = models.TextField(null=False)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    repo = models.CharField(max_length=2048, null=False)
    date_added = models.DateTimeField(default=datetime.now, null=False)

    class Meta:
        unique_together = ('name', 'owner')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk:
            #parse the template

            pass
        # This code only happens if the objects is
        # not in the database yet. Otherwise it would
        # have pk
        super(App, self).save(*args, **kwargs)

