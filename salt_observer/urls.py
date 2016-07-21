from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from .views import (
    Login, Logout,
    Dashboard, VisualNetwork,
    MinionList, MinionDetail, MinionEdit,
    NetworkList, NetworkDetail, NetworkEdit,
    DomainList, DomainDetail, DomainEdit
)


def auth_url(regex, view, *args, **kwargs):
    return url(regex, login_required(view), *args, **kwargs)


urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),

    url(r'^login/$', Login.as_view(), name='login'),
    url(r'^logout/$', Logout.as_view(), name='logout'),

    auth_url(r'^$', Dashboard.as_view(), name='dashboard'),
    auth_url(r'^visual-network/$', VisualNetwork.as_view(), name='visual-network'),

    auth_url(r'^minions/$', MinionList.as_view(), name='minion-list'),
    auth_url(r'^minions/(?P<slug>[a-zA-Z0-9\.\-]+)/$', MinionDetail.as_view(), name='minion-detail'),
    auth_url(r'^minions/(?P<slug>[a-zA-Z0-9\.\-]+)/edit/$', MinionEdit.as_view(), name='minion-edit'),

    auth_url(r'^networks/$', NetworkList.as_view(), name='network-list'),
    auth_url(r'^networks/(?P<slug>[a-zA-Z0-9\.\-]+)/$', NetworkDetail.as_view(), name='network-detail'),
    auth_url(r'^networks/(?P<slug>[a-zA-Z0-9\.\-]+)/edit/$', NetworkEdit.as_view(), name='network-edit'),

    auth_url(r'^domains/$', DomainList.as_view(), name='domain-list'),
    auth_url(r'^domains/(?P<slug>[a-zA-Z0-9\.\-]+)/$', DomainDetail.as_view(), name='domain-detail'),
    auth_url(r'^domains/(?P<slug>[a-zA-Z0-9\.\-]+)/edit/$', DomainEdit.as_view(), name='domain-edit'),
]
