from django.db import models

import json


class MarkdownContent(models.Model):
    ''' To enable on-the-fly modification of templates '''

    md_content = models.TextField()

    class Meta:
        abstract = True


class Network(MarkdownContent):
    ''' Representation of an Network '''

    ipv4 = models.CharField(max_length=15)
    mask = models.CharField(max_length=15)

    last_updated = models.DateTimeField()

    def __str__(self):
        return self.ipv4


class Minion(MarkdownContent):
    ''' Representation of a Server in Salt '''

    fqdn = models.CharField(max_length=255)
    networks = models.ManyToManyField(Network, through='NetworkInterface')
    data = models.TextField(default='{}')

    last_updated = models.DateTimeField()

    @property
    def get_data(self):
        return json.loads(self.data)

    def __str__(self):
        return self.fqdn


class NetworkInterface(models.Model):
    ''' Representing a network card '''

    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    minion = models.ForeignKey(Minion, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    mac_address = models.CharField(max_length=17)

    def __str__(self):
        return '{} ({})'.format(self.name, self.mac_address)
