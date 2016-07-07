from django.core.management.base import BaseCommand
from django.utils import timezone

from salt_observer.models import Minion
from . import ApiCommand

import json


class Command(ApiCommand, BaseCommand):
    help = 'Fetch and save new data from all servers'

    def save_server_users(self, data):
        for minion_fqdn, packages in data.items():
            minion = Minion.objects.filter(fqdn=minion_fqdn).first()

            minion_data = json.loads(minion.data)
            minion_data['users'] = packages
            minion.data = json.dumps(minion_data)

            minion.save()

    def handle(self, *args, **kwargs):
        api = super().handle(*args, **kwargs)

        self.save_server_users(api.get_server_module_data('user.list_users'))

        api.logout()
