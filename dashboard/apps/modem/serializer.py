################    REST Libraries      ##################
from rest_framework import serializers
from rest_framework.serializers import (PrimaryKeyRelatedField,
                                        CurrentUserDefault)

from rest_framework_bulk import (BulkListSerializer,
                                 BulkSerializerMixin,)

################          My code       ##################
from .models import Message, Contact


class MessageSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
    class Meta:
        model = Message
        exclude = ('id','user','created_on' )
        list_serializer_class = BulkListSerializer


class ContactSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    user = PrimaryKeyRelatedField(read_only=True, default=CurrentUserDefault())
    class Meta:
        model = Message
        exclude = ('id','user','created_on' )
        list_serializer_class = BulkListSerializer
