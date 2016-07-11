from django.core.management.base import BaseCommand

from salt_observer.models import Minion
from . import ApiCommand

import json


class Command(ApiCommand, BaseCommand):
    help = 'Fetch and save mount points data'

    def save_packages(self, api):
        mount_point_devices = api.get_server_module_data('ps.disk_partition_usage')

        for minion_fqdn, devices in mount_point_devices.items():

            minion = Minion.objects.filter(fqdn=minion_fqdn).first()
            minion_data = json.loads(minion.data)

            mounted_devices = devices

            minion_data['mounted_devices'] = mounted_devices
            minion.data = json.dumps(minion_data)
            minion.save()

    def handle(self, *args, **kwargs):
        api = super().handle(*args, **kwargs)
        self.save_packages(api)
        api.logout()
