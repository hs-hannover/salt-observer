from django.core.management.base import BaseCommand
from django.utils import timezone

from salt_observer.models import Minion
from . import ApiCommand

import json


class Command(ApiCommand, BaseCommand):
    help = 'Fetch and save new data from all servers'

    def save_packages(self, api):
        print('Fetching packages ...')
        packages = api.get_server_module_data('pkg.list_pkgs')
        print('Fetching upgrades ...')
        upgrades = api.get_server_module_data('pkg.list_upgrades')

        for minion_fqdn, minion_packages in packages.items():

            print('Handling {}'.format(minion_fqdn))

            minion = Minion.objects.filter(fqdn=minion_fqdn).first()
            minion_data = json.loads(minion.data)

            minion_package_data = {}
            for minion_package_name, minion_package_version in minion_packages.items():
                if type(upgrades.get(minion_fqdn, {})) != dict:
                    del upgrades[minion_fqdn]

                minion_package_data.update({
                    minion_package_name: {
                        'version': minion_package_version,
                        'latest_version': upgrades.get(minion_fqdn, {}).get(minion_package_name, '')
                    }
                })

            minion_data['packages'] = minion_package_data
            minion.data = json.dumps(minion_data)
            minion.save()

    def handle(self, *args, **kwargs):
        api = super().handle(*args, **kwargs)
        self.save_packages(api)
        api.logout()
