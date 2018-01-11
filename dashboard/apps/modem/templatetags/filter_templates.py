from django import template

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='mod')
def get_item(number, mod):
    return (number-1)%mod

@register.filter(name='get_msg_item')
def get_item(message, item):
    return getattr(message, item)

@register.filter(name ="key")
def key_ (dictionary):
    return dictionary.keys()#[0]
