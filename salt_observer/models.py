from django.db import models


class Network(models.Model):
    ''' Representation of an Network '''

    net = models.CharField(max_length=15)
    subnet_mask = models.CharField(max_length=15)


class Minion(models.Model):
    ''' Representation of a Server in Salt '''

    name = models.CharField(max_length=255)
