from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.
class Message(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now_add=True)
class Message2(models.Model):
    text = models.TextField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE , related_name='owner')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete = models.CASCADE , related_name='recipient')
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(auto_now_add=True)