from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.template.context import RequestContext
from collections import defaultdict, Counter
from django.http import JsonResponse


#############   REST Libraries      ##########
from rest_framework import permissions
from rest_framework import generics
from rest_framework_bulk import ListBulkCreateUpdateDestroyAPIView
#############      My libraries     ##########
from .serializer import MessageSerializer, ContactSerializer, MessageQueueSerializer
from .models     import Message, Contact, MessageQueue

############## Constants  ##############
from .models     import (MSG_SENT, MSG_FAILED, MSG_RESEND, MSG_ARCHIVED, MSG_QUEUED,
                        CONTACT_CHANGE, CONTACT_NORMAL)



#############     Auxiliar functions  #############
def create_home_dictionary(query):
    tmp_dic = {}
    result_dic = {}
    for item in query:
        key = item.last_attempt.strftime("%Y-%m-%d")
        tmp_dic[item.queue.number] = {key:0}

    for item in query:
        key = item.last_attempt.strftime("%Y-%m-%d")
        tmp_dic[item.queue.number][key] += 1

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
    for queue in MessageQueue.objects.all():
        tmp_dic[queue.number] = []
    for item in query:
        tmp_dic[item.queue.number].append(item)
    return tmp_dic


@login_required
def home(request):

    ctx = {
        'failed': create_home_dictionary(Message.objects.filter(status=MSG_FAILED)),
        'sent'  : create_home_dictionary(Message.objects.filter(status=MSG_SENT)),
        'queued': create_home_dictionary(Message.objects.filter(status=MSG_QUEUED))
        }
    data ={"data":ctx}
    return render(request, 'home.html',data)

@login_required
def queues(request):
    raw_queues = MessageQueue.objects.filter(is_active=True)
    queues = raw_queues.values("number").distinct()
    msg_fail = ''
    msg_success = ''

    if request.method == 'POST':
        #Delete message, or resend or resend with another queue
        for queue in queues:
            queue_item = str(queue["number"])
            list_msgs = request.POST.getlist("selected_"+ queue_item)
            # Resend with another queue
            if list_msgs and 'btnMove' in request.POST:
                new_queue_value = request.POST["queue_"+queue_item]
                if list_msgs and  new_queue_value =="empty":
                    msg_fail = "No se puede mover a cola vacia"
                else:
                    new_queue_value = int(new_queue_value)
                    for id_msg  in list_msgs:
                        msg_item = Message.objects.get(id=id_msg)
                        msg_item.queue= [q for q in raw_queues if q.number == new_queue_value][0]
                        msg_item.status = MSG_RESEND
                        msg_item.save()
                    msg_success = "#%d mensajes movidos a la cola %s"%(len(list_msgs),new_queue_value)
            # Archive message
            if list_msgs and 'btnDelete' in request.POST:
                for id_msg in list_msgs:
                    msg_item = Message.objects.get(id=id_msg)
                    msg_item.status = MSG_ARCHIVED
                    msg_item.save()

    ctx = {'failed': create_queued_dictionary(Message.objects.filter(status=MSG_FAILED)),
            'queues': queues,
            'msg_success':msg_success,
            'msg_fail': msg_fail}

    return render(request, 'queues.html',ctx)

@login_required
def messages(request):

    ctx = {'failed': create_queued_dictionary(Message.objects.filter(status=MSG_FAILED))}
    return render(request, 'messages.html',ctx)

@login_required
def contacts(request):
    #Return contacts by queue
    msg_fail = ''
    msg_success = ''
    raw_queues = MessageQueue.objects.filter(is_active=True)
    queues = raw_queues.values("number").distinct()

    if request.method == 'POST':
        #Change contact
        for queue in queues:
            queue_item = str(queue["number"])
            list_contact = request.POST.getlist("selected_"+ queue_item)
            # Resend with another queue
            if list_contact and 'btnMove' in request.POST:
                new_queue_value = request.POST["queue_"+queue_item]
                if list_contact and  new_queue_value =="empty":
                    msg_fail = "No se puede mover a cola vacia"
                else:
                    new_queue_value = int(new_queue_value)
                    for id_contact  in list_contact:
                        contact_item = Contact.objects.get(id=id_contact)
                        contact_item.queue= [q for q in raw_queues if q.number == new_queue_value][0]
                        contact_item.status = CONTACT_CHANGE
                        contact_item.save()
                    msg_success = "#%d contacto movidos al slot %s"%(len(list_contact),new_queue_value)

    ctx = { 'failed': create_queued_dictionary(Contact.objects.filter()),
            'msg_success':msg_success,
            'queues': queues,
            'msg_fail': msg_fail}
    return render(request, 'contacts.html',ctx)



@login_required
def contact_moved(request):
    contacts = Contact.objects.filter(status = CONTACT_CHANGE)
    to_json = [{"contact":contact.contact, "queue": contact.queue.number} for contact in contacts]
    for contact in contacts:
        contact.status = CONTACT_NORMAL
        contact.save()
    return JsonResponse(to_json,safe=False)

###############    REST API    ################

class MessageViewSet(ListBulkCreateUpdateDestroyAPIView):

    serializer_class = MessageSerializer

    def get_queryset(self):
        status = self.kwargs['status']
        print(status)
        queryset = Message.objects.filter(status = status)
        return queryset



class ContactViewSet(ListBulkCreateUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

class MessageQueueViewSet(ListBulkCreateUpdateDestroyAPIView):
    queryset = MessageQueue.objects.all()
    serializer_class = MessageQueue
