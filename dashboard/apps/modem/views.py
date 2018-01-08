from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext


#############   REST Libraries      ##########
from rest_framework import permissions
from rest_framework import generics
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView
#############      My libraries     ##########
from .serializer import MessageSerializer
from .models     import Message

@login_required
def home(request):
    ctx = {
            'historic': True,
        }
    return render(request, 'home.html',ctx)

class MessageViewSet(ListBulkCreateUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
