from django.contrib import admin

from .models import *

class MessageAdmin(admin.ModelAdmin):
    list_display = ('message','contact_contact' ,'queue_number', 'status' )
    def contact_contact(self, instance):
        return instance.contact.contact

    def queue_number(self,instance):
        return instance.queue.number

class ContactAdmin(admin.ModelAdmin):
    list_display =('contact', 'queue_number', 'status')

    def queue_number(self,instance):
        return instance.queue.number

class QueueMessageAdmin(admin.ModelAdmin):
    list_display = ('number', 'is_active')

admin.site.register(Message, MessageAdmin)
admin.site.register(MessageQueue, QueueMessageAdmin)
admin.site.register(Contact, ContactAdmin)
