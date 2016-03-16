from django.core.management.base import BaseCommand, CommandError

from salt_observer.cherry import SaltCherrypyApi
from salt_observer.models import Minion

from getpass import getpass
import json


class Command(BaseCommand):
    help = 'Fetch and save new data from all servers'

    def handle(self, *args, **options):
        m = SaltCherrypyApi(input('Username: '), getpass())

        all_grains = m.get_server_information()

        for minion_fqdn, minion_grains in all_grains.items():
            minion = Minion.objects.filter(fqdn=minion_fqdn).first()

            self.stdout.write('{:>50} '.format(minion_fqdn), ending='')

            if minion:
                self.stdout.write(self.style.SUCCESS('Found'))
                minion.grains = json.dumps(minion_grains)
                minion.save()
            else:
                self.stdout.write(self.style.WARNING('New'))
                Minion(
                    fqdn=minion_fqdn,
                    grains=json.dumps(minion_grains)
                ).save()

        m.logout()
