from django.template import Context, Template
from django.views.generic import View, TemplateView
from django.views.generic.list import ListView
from django.utils.safestring import mark_safe
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from markdown import Markdown

from salt_observer.models import Minion, Network


class Dashboard(TemplateView):
    template_name = 'dashboard.html'


class MinionList(ListView):
    template_name = 'minion/list.html'
    model = Minion


class MinionDetail(View):

    def get(self, request, minion_fqdn, *args, **kwargs):
        minion = Minion.objects.filter(fqdn=minion_fqdn).first()

        c = {'minion': minion}
        c['minion'].grains = minion.get_grains

        plain_text = Template('{% extends "docs/minion.md" %}\n\n' + minion.md_content).render(Context(c))
        md = Markdown(extensions=['markdown.extensions.toc', 'markdown.extensions.extra'])

        c.update({'md_html': mark_safe(md.convert(plain_text)), 'toc': mark_safe(md.toc)})
        return render(request, 'minion/detail.html', c)


class NetworkList(ListView):
    template_name = 'network/list.html'
    model = Network


class NetworkDetail(View):

    def get(self, request, network_ipv4, *args, **kwargs):
        network = Network.objects.filter(ipv4=network_ipv4).first()

        c = {'network': network}

        plain_text = Template('{% extends "docs/network.md" %}\n\n' + network.md_content).render(Context(c))
        md = Markdown(extensions=['markdown.extensions.toc', 'markdown.extensions.extra'])

        c.update({'md_html': mark_safe(md.convert(plain_text)), 'toc': mark_safe(md.toc)})
        return render(request, 'network/detail.html', c)
