"""django_template URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rest_framework.authtoken import views
from django.conf.urls import  include, url

from apps.userprofile import views as userprofile_views
from apps.modem import views as modem_views
from apps.modem.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signin/$', userprofile_views.signin),
    url(r'^accounts/login/', userprofile_views.signin),
    url(r'^home/', modem_views.home),
    url(r'^queues/$', modem_views.queues),
    url(r'^messages/$', modem_views.messages),
    url(r'^contacts/$', modem_views.contacts),
    ##### Urls to use with modem
    url(r'^add_message/', MessageViewSet.as_view()),
    url(r'^add_message/(?P<status>.)/', MessageViewSet.as_view()),
    url(r'^add_contact/', ContactViewSet.as_view()),
    url(r'^add_queue/', MessageQueueViewSet.as_view()),
    url(r'^move_contact/', modem_views.contact_moved)

]
