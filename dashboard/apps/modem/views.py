from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from collections import defaultdict, Counter


#############   REST Libraries      ##########
from rest_framework import permissions
from rest_framework import generics
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView
#############      My libraries     ##########
from .serializer import MessageSerializer, ContactSerializer
from .models     import Message, Contact



#############     Auxiliar functions  #############
def create_home_dictionary(query):
    tmp_dic = {}
    result_dic = {}
    for item in query:
        key = item.last_attempt.strftime("%Y-%m-%d")
        tmp_dic[item.queue] = {key:0}

    for item in query:
        key = item.last_attempt.strftime("%Y-%m-%d")
        tmp_dic[item.queue][key] += 1

    labels =[]
    for queue in tmp_dic.keys():
        result_dic[queue] = []
        labels = []
        for k,v in tmp_dic[queue].items():
            result_dic[queue].append(v)
            labels.append(k)
    result_dic["labels"] = labels
    return result_dic


def create_queued_dictionary(query):
    tmp_dic = {}
    for item in query:
        if item.queue in tmp_dic:
            tmp_dic[item.queue].append(item)
        else:
            tmp_dic[item.queue] = [item]
    return tmp_dic

@login_required
def home(request):

    ctx = {
        'failed': create_home_dictionary(Message.objects.filter(status="F")),
        'sent'  : create_home_dictionary(Message.objects.filter(status="S")),
        'queued': create_home_dictionary(Message.objects.filter(status="Q"))
        }
    data ={"data":ctx}
    return render(request, 'home.html',data)

@login_required
def queues(request):
    ctx = {'failed': create_queued_dictionary(Message.objects.filter(status="F"))}
    return render(request, 'queues.html',ctx)

@login_required
def messages(request):
    ctx = {'failed': create_queued_dictionary(Message.objects.filter(status="F"))}
    return render(request, 'messages.html',ctx)


class MessageViewSet(ListBulkCreateUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class ContactViewSet(ListBulkCreateUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
