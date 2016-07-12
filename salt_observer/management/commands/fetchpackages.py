from django.core.management.base import BaseCommand

from salt_observer.models import Minion
from . import ApiCommand

import json


class Command(ApiCommand, BaseCommand):
    help = 'Fetch and save packagedata'

    def save_packages(self, api):
        packages = api.get('pkg.list_pkgs')
        upgrades = api.get('pkg.list_upgrades')

        for minion_fqdn, minion_packages in packages.items():

            minion = Minion.objects.filter(fqdn=minion_fqdn).first()

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

            minion.update_data({'packages': minion_package_data})
            minion.save()

    def handle(self, *args, **kwargs):
        api = super().handle(*args, **kwargs)
        self.save_packages(api)
        api.logout()
