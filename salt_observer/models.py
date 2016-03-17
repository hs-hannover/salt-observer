from django.db import models

import json


class Network(models.Model):
    ''' Representation of an Network '''

    ipv4 = models.CharField(max_length=15)
    mask = models.CharField(max_length=15)

    def __str__(self):
        return self.ipv4


class Minion(models.Model):
    ''' Representation of a Server in Salt '''

    fqdn = models.CharField(max_length=255)
    networks = models.ManyToManyField(Network, through='NetworkCard')
    grains = models.TextField()

    @property
    def get_grains(self):
        return json.loads(self.grains)

    def __str__(self):
        return self.fqdn


class NetworkCard(models.Model):
    ''' Representing a network card '''

    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    minion = models.ForeignKey(Minion, on_delete=models.CASCADE)

    mac_address = models.CharField(max_length=17)

    def __str__(self):
        return self.mac_address
