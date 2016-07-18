from django.template import Context, Template
from django.views.generic import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from markdown import Markdown

from salt_observer.models import (
    Minion, Network, Domain
)


class Dashboard(TemplateView):
    template_name = 'dashboard.html'


class MinionList(ListView):
    template_name = 'minion/list.html'
    model = Minion


class NetworkList(ListView):
    template_name = 'network/list.html'
    model = Network


class MinionDetail(DetailView):
    template_name = 'minion/detail.html'
    model = Minion
    slug_field = 'fqdn'


class NetworkDetail(DetailView):
    template_name = 'network/detail.html'
    model = Network
    slug_field = 'ipv4'


class DomainList(ListView):
    template_name = 'domain/list.html'
    model = Domain


class DomainDetail(DetailView):
    template_name = 'domain/detail.html'
    model = Domain
    slug_field = 'fqdn'
