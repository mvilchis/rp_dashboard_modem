# -*- codiging: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.dispatch import receiver

MSG_FAILED   = "F"
MSG_SENT     = "S"
MSG_QUEUED   = "Q"
MSG_RESEND   = "R"
MSG_ARCHIVED = "A"

CONTACT_NORMAL = "N"
CONTACT_CHANGE = "C"
CONTACT_STATUS  = ((CONTACT_NORMAL, CONTACT_NORMAL), (CONTACT_CHANGE, CONTACT_CHANGE))

MSG_STATUS = ((MSG_FAILED   ,MSG_FAILED   ), (MSG_SENT     ,MSG_SENT     ), (MSG_QUEUED ,MSG_QUEUED   ), (MSG_RESEND   ,MSG_RESEND   ), (MSG_ARCHIVED ,MSG_ARCHIVED ) )


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class MessageQueue(models.Model):
    """ Class to represent a message_queue """
    is_active = models.BooleanField(default = True)
    number = models.IntegerField()

class Contact(models.Model):
    """ Class to represent a contact """
    contact      = models.CharField(max_length=250, blank=True, null=True)
    queue        = models.ForeignKey(MessageQueue)
    status       = models.CharField(max_length = 3,
                                    blank=True,
                                    null=True,
                                    choices =CONTACT_STATUS,
                                    default=CONTACT_NORMAL)
    is_prospera  = models.BooleanField(default = False)

class Message(models.Model):
    """ Class to represent a message from modem gsm
          > status: F(failed), S(send), Q(queued), R(resend), A(archived)
          > queue: index of queue
    """
    user         = models.ForeignKey(User, null=True)
    message      = models.CharField(max_length=250, blank=True, null=True)
    contact      = models.ForeignKey(Contact)
    last_attempt = models.DateField(blank=True, null=True)
    created_on   = models.DateTimeField(auto_now_add=True, blank=True)
    status       = models.CharField(max_length=3, blank=True,
                                    null=True, choices = MSG_STATUS )
    queue        = models.ForeignKey(MessageQueue)
