from django.template import Context, Template
from django.views.generic import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse_lazy
from django.utils.safestring import mark_safe
from django.contrib.auth import login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

from markdown import Markdown

from salt_observer.forms import LoginForm
from salt_observer.models import (
    Minion, Network, Domain
)


class Login(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form, *args, **kwargs):
        login(self.request, form.get_user())
        return super().form_valid(form, *args, **kwargs)

    def get_success_url(self):
        return self.request.GET.get('next', reverse_lazy('dashboard'))

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('dashboard'))
        else:
            return super().dispatch(request, *args, **kwargs)


class Logout(View):

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('dashboard'))


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
