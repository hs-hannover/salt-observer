from django.core.management.base import BaseCommand

from salt_observer.models import Minion
from . import ApiCommand


class Command(ApiCommand, BaseCommand):
    help = 'Fetch and save listening network services'

    def save_services(self, api):
        listening_services = api.get('network.netstat')

        for minion_fqdn, services in listening_services.items():
            minion = Minion.objects.filter(fqdn=minion_fqdn).first()

            if not minion:
                continue

            minion_services = []
            for service in services:
                if service.get('state', '') == 'LISTEN':
                    minion_services.append(service)

            minion.update_data({'listening_services': minion_services})
            minion.save()

    def handle(self, *args, **kwargs):
        api = super().handle(*args, **kwargs)
        self.save_services(api)
        api.logout()
