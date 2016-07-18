from django.core.management.base import BaseCommand

from salt_observer.models import Domain
from salt_observer.ssllabs import SSLLabsApi


class Command(BaseCommand):
    help = 'Fetch and save grades for domains from ssllabs'

    def handle(self, *args, **kwargs):
        domain_list = [d.fqdn for d in Domain.objects.all().filter(can_speak_https=True, public=True, valid=True)]
        status_list = SSLLabsApi().check_domains(domain_list)

        for fqdn, status in status_list.items():
            domain = Domain.objects.filter(fqdn=fqdn).first()
            domain.ssl_lab_status = status
            domain.save()
