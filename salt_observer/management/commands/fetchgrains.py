from django.core.management.base import BaseCommand
from django.utils import timezone

from salt_observer.models import Minion, Network, NetworkInterface
from . import ApiCommand

import netaddr
import json


class Command(ApiCommand, BaseCommand):
    help = 'Fetch and save new data from all servers'

    def _update_data(self, grains):
        ''' Update everything we can update out of the grains '''
        touched = {'minions': [], 'networks': [], 'interfaces': []}
        for minion_fqdn, minion_grains in grains.items():
            minion = self._update_minion(minion_fqdn, minion_grains)
            touched['minions'].append(minion)

            if 'so_interfaces' in minion_grains.keys():
                self._update_connections(minion_grains['so_interfaces'], minion, touched)
        return touched

    def _update_minion(self, fqdn, grains):
        ''' Update minions related to grains we got '''
        minion = Minion.objects.filter(fqdn=fqdn).first()
        if minion:
            data = json.loads(minion.data)
            data['grains'] = grains
            minion.data = json.dumps(data)
            minion.last_updated = timezone.now()
        else:
            minion = Minion(fqdn=fqdn, data=json.dumps({'grains': grains}), last_updated=timezone.now())
        minion.save()
        return minion

    def _update_connections(self, interfaces, minion, touched):
        ''' Update networks and network interfaces '''
        for if_name, if_data in interfaces.items():
            if if_name in ['lo', 'lo0']:
                continue

            ipv4_network = str(netaddr.IPNetwork('{}/{}'.format(if_data['ipv4']['address'], if_data['ipv4']['netmask'])).network)
            network = self._update_network(ipv4_network, if_data['ipv4']['netmask'])
            touched['networks'].append(network)
            interface = self._update_network_interface(network, minion, if_data['mac_address'], if_name)
            touched['interfaces'].append(interface)

    def _update_network(self, ipv4, mask):
        ''' Update the Network objects '''
        network = Network.objects.filter(ipv4=ipv4).first()
        if not network:
            network = Network(ipv4=ipv4, mask=mask, last_updated=timezone.now())
        else:
            network.last_updated = timezone.now()
        network.save()
        return network

    def _update_network_interface(self, network, minion, mac_address, if_name):
        ''' Update all network interfaces '''
        ni = NetworkInterface.objects.filter(network=network, minion=minion, mac_address=mac_address).first()
        if not ni:
            ni = NetworkInterface(network=network, minion=minion, mac_address=mac_address, name=if_name).save()
        return ni

    def _cleanup(self, touched):
        for minion in Minion.objects.all():
            if minion not in touched['minions']:
                minion.delete()
        for network in Network.objects.all():
            if network not in touched['networks']:
                network.delete()
        for interface in NetworkInterface.objects.all():
            if interface not in touched['interfaces']:
                interface.delete()

    def handle(self, *args, **kwargs):
        api = super().handle(*args, **kwargs)

        touched_elements = self._update_data(api.get('grains.items'))
        self._cleanup(touched_elements)

        api.logout()
