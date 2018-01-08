# -*- codiging: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class Message(models.Model):
    """ Class to represent a message from modem gsm
          > status: F(failed), S(send), Q(queued)
          > queue: index of queue
    """
    user         = models.ForeignKey(User, null=True)
    message      = models.CharField(max_length=250, blank=True, null=True)
    contact      = models.CharField(max_length=250, blank=True, null=True)
    last_attempt = models.DateField(blank=True, null=True)
    created_on   = models.DateTimeField(auto_now_add=True, blank=True)
    status       = models.CharField(max_length=3, blank=True, null=True)
    queue        = models.IntegerField()
