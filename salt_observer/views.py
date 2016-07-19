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

from markdown import Markdown

from salt_observer.forms import (
    LoginForm,
    MinionEditForm, NetworkEditForm, DomainEditForm
)
from salt_observer.models import (
    Minion, Network, Domain
)


class MarkdownEditMixin(object):

    def form_valid(self, form, *args, **kwargs):
        obj = self.get_object()
        obj.md_content = form.cleaned_data.get('md_content', '')
        obj.md_last_autor = self.request.user
        obj.md_last_edited = timezone.now()
        obj.save()
        return super().form_valid(form, *args, **kwargs)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy(self.success_url_name, args=[self.kwargs.get('slug', '')])


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
