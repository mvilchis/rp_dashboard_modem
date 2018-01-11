################    REST Libraries      ##################
from rest_framework import serializers
from rest_framework.serializers import (PrimaryKeyRelatedField,
                                        CurrentUserDefault)

from rest_framework_bulk import (BulkListSerializer,
                                 BulkSerializerMixin,)

################          My code       ##################
from .models import Message, Contact, MessageQueue


class MessageSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
    queue_number =  serializers.CharField(source="queue.number")
    contact_number =  serializers.CharField(source="contact.contact")

    class Meta:
        model = Message
        exclude = ('id','user','created_on' ,'queue', 'contact')
        list_serializer_class = BulkListSerializer

    def create(self, validated_data):
        message_queue = validated_data.pop('queue')["number"]
        message_contact = validated_data.pop('contact')["contact"]
        validated_data["queue"]= MessageQueue.objects.get(number=message_queue)
        validated_data["contact"]= Contact.objects.get(contact=message_contact)
        msg = Message.objects.create(**validated_data)
        msg.save()
        return msg


class ContactSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
    queue_number =  serializers.CharField(source="queue.number")

    class Meta:
        model = Contact
        exclude = ('id','user','queue')
        list_serializer_class = BulkListSerializer

    def create(self, validated_data):
        message_queue = validated_data.pop('queue')["number"]
        validated_data["queue"]= MessageQueue.objects.get(number=message_queue)
        number = validated_data.pop('contact')
        #Check if exist:
        contact = Contact.objects.filter(contact = number)
        if contact:
            contact = contact.first()
            contact.queue = validated_data["queue"]
            contact.status = validated_data["status"]
            contact.save()
            return contact
        validated_data["contact"] = number
        contact = Contact.objects.create(**validated_data)
        contact.save()
        return contact


class MessageQueueSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())

    class Meta:
        model = MessageQueue
        exclude = ('id','user','created_on' )
        list_serializer_class = BulkListSerializer
