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

#############     Auxiliar functions  #############
def create_dictionary(query):
    result_dic = {}
    for item in query:
        if item.queue in result_dic:
            result_dic[item.queue].append(item)
        else:
            result_dic[item.queue] = [item]
    return result_dic

@login_required
def home(request):
    ctx = {
        'failed': create_dictionary(Message.objects.filter(status="F")),
        'sent'  : create_dictionary(Message.objects.filter(status="S")),
        'queued': create_dictionary(Message.objects.filter(status="Q"))
        }
    print (ctx)
    return render(request, 'home.html',ctx)

class MessageViewSet(ListBulkCreateUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
