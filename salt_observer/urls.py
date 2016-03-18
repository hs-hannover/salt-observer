from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from .views import (
    Dashboard,
    MinionList, MinionDetail,
    NetworkList, NetworkDetail,
)


def auth_url(regex, view, *args, **kwargs):
    return url(regex, login_required(view), *args, **kwargs)


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),

    url(r'^$', Dashboard.as_view(), name='dashboard'),
    url(r'^minions/$', MinionList.as_view(), name='minion-list'),
    url(r'^minions/(?P<minion_fqdn>[a-zA-Z0-9\.\-]+)/$', MinionDetail.as_view(), name='minion-detail'),

    url(r'^minions/$', NetworkList.as_view(), name='network-list'),
    url(r'^minions/(?P<minion_fqdn>[a-zA-Z0-9\.\-]+)/$', NetworkDetail.as_view(), name='network-detail'),
]
