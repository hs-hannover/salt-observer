from django.contrib.auth.models import User
from django.template import Context, Template
from django.views.generic import View, TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.core.urlresolvers import reverse_lazy
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.auth import login, logout
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings

import json
from markdown import Markdown
from collections import OrderedDict
from dateutil.parser import parse as dateparse

from salt_observer.saltapis import SaltTornado
from salt_observer.forms import (
    LoginForm,
    MinionEditForm, NetworkEditForm, DomainEditForm
)
from salt_observer.models import (
    Minion, Network, Domain
)


class MarkdownEditMixin(object):

    def form_valid(self, form, *args, **kwargs):
        result = super().form_valid(form, *args, **kwargs)
        obj = self.get_object()

        obj.md_content = form.cleaned_data.get('md_content', '')
        obj.md_last_autor = self.request.user
        obj.md_last_edited = timezone.now()
        obj.save()

        return result

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy(self.success_url_name, args=[self.kwargs.get('slug', '')])


class Login(FormView):
    template_name = 'auth/login.html'
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form, *args, **kwargs):
        login(self.request, form.get_user())
        return super().form_valid(form, *args, **kwargs)

    def get_form_kwargs(self, *args, **kwargs):
        '''dirty hack to pass the current request down to the backends'''
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs['request'] = self.request
        return kwargs

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
    template_name = 'home/dashboard.html'

    def get_context_data(self, *args, **kwargs):
        all_minions = Minion.objects.all()
        all_networks = Network.objects.all()
        all_domains = Domain.objects.all()

        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'all_minions': all_minions,
            'all_networks': all_networks,
            'all_domains': all_domains,
            'all_users': User.objects.all(),
            'w5_outdated_minions': sorted(all_minions, key=lambda m: m.outdated_package_count(), reverse=True)[:5],
            'w5_fullest_minions': sorted(all_minions, key=lambda m: m.fullest_partition_percentage(), reverse=True)[:5],
            'w5_domain_ssl_grades': sorted(all_domains, key=lambda d: d.worst_grade(), reverse=True)[:5],
        })
        return ctx


class VisualNetwork(TemplateView):
    template_name = 'home/visual_network.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({
            'minions': Minion.objects.all(),
            'networks': Network.objects.all().exclude(ipv4=settings.SALT_NETWORK),
        })
        return ctx


class MinionList(ListView):
    template_name = 'minion/list.html'
    model = Minion


class MinionDetail(DetailView):
    template_name = 'minion/detail.html'
    model = Minion
    slug_field = 'fqdn'


class MinionEdit(MarkdownEditMixin, UpdateView, MinionDetail):
    template_name = 'minion/edit.html'
    form_class = MinionEditForm
    success_url_name = 'minion-detail'


class NetworkList(ListView):
    template_name = 'network/list.html'
    model = Network


class NetworkDetail(DetailView):
    template_name = 'network/detail.html'
    model = Network
    slug_field = 'ipv4'


class NetworkEdit(MarkdownEditMixin, UpdateView, NetworkDetail):
    template_name = 'network/edit.html'
    form_class = NetworkEditForm
    success_url_name = 'network-detail'


class DomainList(ListView):
    template_name = 'domain/list.html'
    model = Domain


class DomainDetail(DetailView):
    template_name = 'domain/detail.html'
    model = Domain
    slug_field = 'fqdn'


class DomainEdit(MarkdownEditMixin, UpdateView, DomainDetail):
    template_name = 'domain/edit.html'
    form_class = DomainEditForm
    success_url_name = 'domain-detail'


class AbstractTornadoView(TemplateView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'tornado_host': settings.SALT['api']['tornado']['host'],
            'tornado_port': settings.SALT['api']['tornado']['port'],
        })
        return context


class EventView(AbstractTornadoView):
    template_name = 'events.html'


class JobView(AbstractTornadoView):
    template_name = 'jobs/index.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'job_list': self.transform_jobs(self.get_jobs())
        })
        return context

    def get_jobs(self):
        return SaltTornado(
            token=self.request.session['salt_tornado_token']
        ).request(
            resource='/jobs/'
        ).json().get('return')[0]

    def transform_jobs(self, jobs):
        transformed_jobs = dict()

        for key, value in jobs.items():
            value['StartTime'] = dateparse(value['StartTime'])
            if not value['Function'] in settings.SALT['jobs']['ignore']:
                transformed_jobs.update({key: value})

        return OrderedDict(sorted(transformed_jobs.items(), reverse=True))


class JobDetailView(AbstractTornadoView):
    template_name = 'jobs/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'job_details': SaltTornado(
                token=self.request.session['salt_tornado_token']
            ).request(
                resource='/jobs/' + str(kwargs['jid']),
            ).json().get('return')[0]
        })
        return context
