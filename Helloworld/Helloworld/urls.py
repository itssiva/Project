from django.conf.urls import include, url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', home, name='home'),
    url(r'^v1/logs/?$', v1_logs, name='logs'),
    url(r'^v1/hello-world/?$', v1_helloworld, name='hello_world'),
    url(r'^v1/hello-world/logs/?$', v1_helloworld_logs, name='logs_hello_world'),
    url(r'^v1/', default, name='default'),
]
