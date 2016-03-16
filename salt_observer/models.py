from django.db import models

import json


class Network(models.Model):
    ''' Representation of an Network '''

    net = models.CharField(max_length=15)
    subnet_mask = models.CharField(max_length=15)


class Minion(models.Model):
    ''' Representation of a Server in Salt '''

    fqdn = models.CharField(max_length=255)
    grains = models.TextField()

    @property
    def get_grains(self):
        return json.loads(self.grains)

    def __str__(self):
        return self.fqdn
