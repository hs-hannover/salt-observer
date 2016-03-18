from django.core.management.base import BaseCommand, CommandError

from salt_observer.cherry import SaltCherrypyApi
from salt_observer.models import Minion, Network, NetworkInterface

from getpass import getpass
from datetime import datetime
import netaddr
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
                self.stdout.write(self.style.SUCCESS('Update'))
                minion.grains = json.dumps(minion_grains)
            else:
                self.stdout.write(self.style.WARNING('Create'))
                minion = Minion(
                    fqdn=minion_fqdn,
                    grains=json.dumps(minion_grains),
                    timestamp=datetime.now()
                )
            minion.save()

            if 'so_interfaces' not in minion_grains.keys():
                continue

            for if_name, if_data in minion_grains['so_interfaces'].items():
                if if_name in ['lo', 'lo0']:
                    continue

                ipv4_network = str(netaddr.IPNetwork('{}/{}'.format(if_data['ipv4']['address'], if_data['ipv4']['netmask'])).network)

                self.stdout.write('{:>50} '.format(ipv4_network), ending='')
                network = Network.objects.filter(ipv4=ipv4_network).first()
                if not network:
                    self.stdout.write(self.style.WARNING('Create'))
                    network = Network(ipv4=ipv4_network, mask=if_data['ipv4']['netmask'])
                else:
                    self.stdout.write(self.style.SUCCESS('Update'))
                network.save()

                self.stdout.write('{:>50} '.format(if_data['mac_address']), ending='')
                ni = NetworkInterface.objects.filter(network=network, minion=minion, mac_address=if_data['mac_address']).first()
                if not ni:
                    self.stdout.write(self.style.WARNING('Create'))
                    ni = NetworkInterface(network=network, minion=minion, mac_address=if_data['mac_address'], name=if_name)
                else:
                    self.stdout.write(self.style.SUCCESS('Update'))
                ni.save()

        m.logout()