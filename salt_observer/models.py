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


class Domain(models.Model):
    ''' Represents a Fully qualified domain name '''

    fqdn = models.CharField(max_length=255)
    minion = models.ManyToManyField('Minion', blank=True)

    can_speak_https = models.BooleanField(help_text='Is there a service listening on port 443')
    public = models.BooleanField(help_text='Is this domain public accessible')

    def minion_count(self):
        return len(self.minion.all())

    def __str__(self):
        return self.fqdn


class Minion(MarkdownContent):
    ''' Representation of a Server in Salt '''

    fqdn = models.CharField(max_length=255)
    networks = models.ManyToManyField(Network, through='NetworkInterface')
    _data = models.TextField(default='{}')

    last_updated = models.DateTimeField()

    @property
    def data(self):
        try:
            return json.loads(self._data)
        except ValueError:
            return dict()

    @data.setter
    def data(self, value):
        self._data = json.dumps(value)

    def update_data(self, value):
        ''' In order to update self.data without 3 lines of code
            self.data.update() wont work!
        '''
        data = self.data
        data.update(value)
        self.data = data

    @property
    def user_count(self):
        return len(self.data.get('grains', {}).get('users', []))

    @property
    def package_count(self):
        return len(self.data.get('packages', []))

    @property
    def network_count(self):
        return len(self.networks.all())

    def outdated_package_count(self):
        return len([p for p, v in self.data.get('packages', {}).items() if v['latest_version']])

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
