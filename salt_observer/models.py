from django.db import models
from django.conf import settings

import json
import requests


class MarkdownContent(models.Model):
    ''' To enable on-the-fly modification of templates '''

    md_content = models.TextField(blank=True)
    md_last_edited = models.DateTimeField()
    md_last_autor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    class Meta:
        abstract = True


class Network(MarkdownContent):
    ''' Representation of an Network '''

    ipv4 = models.CharField(max_length=15)
    mask = models.CharField(max_length=15)

    last_updated = models.DateTimeField()

    def __str__(self):
        return self.ipv4


class Domain(MarkdownContent):
    ''' Represents a Fully qualified domain name '''

    fqdn = models.CharField(max_length=255)
    minion = models.ManyToManyField('Minion', blank=True)
    _ssl_lab_status = models.TextField(default='{}')

    can_speak_https = models.BooleanField(help_text='Is there a service listening on port 443')
    public = models.BooleanField(help_text='Is this domain public accessible')
    valid = models.BooleanField()

    @property
    def ssl_lab_status(self):
        try:
            return json.loads(self._ssl_lab_status)
        except ValueError:
            return dict()

    @ssl_lab_status.setter
    def ssl_lab_status(self, value):
        self._ssl_lab_status = json.dumps(value)

    def check_if_valid(self, commit=True):
        try:
            a = requests.get('http://{}/'.format(self.fqdn), timeout=5, verify=False)
            b = requests.get('https://{}/'.format(self.fqdn), timeout=5, verify=False)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            self.valid = False
        else:
            self.valid = True

        if commit:
            self.save()

    def minion_count(self):
        return len(self.minion.all())

    def worst_grade(self):
        if self.ssl_lab_status.get('grades', []):
            return max([g for g in self.ssl_lab_status.get('grades', [])])
        return '0'

    def save(self, *args, **kwargs):
        if not self.id:
            self.check_if_valid(commit=False)
        super().save(*args, **kwargs)

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

    def fullest_partition_percentage(self):
        try:
            return max([p.get('percent', 0) for p in self.data.get('mounted_devices', [])])
        except AttributeError:
            return 0

    def __str__(self):
        return self.fqdn


class NetworkInterface(models.Model):
    ''' Representing a network card '''

    network = models.ForeignKey(Network, on_delete=models.CASCADE)
    minion = models.ForeignKey(Minion, on_delete=models.CASCADE)

    name = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=17)
    mac_address = models.CharField(max_length=17)

    def __str__(self):
        return '{} ({})'.format(self.name, self.mac_address)
