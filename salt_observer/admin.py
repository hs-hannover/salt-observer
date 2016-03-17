from django.contrib import admin

from salt_observer.models import Minion, Network


class MinionAdmin(admin.ModelAdmin):
    readonly_fields = ('fqdn', 'grains',)
admin.site.register(Minion, MinionAdmin)


class NetworkAdmin(admin.ModelAdmin):
    readonly_fields = ('ipv4', 'mask')
admin.site.register(Network, NetworkAdmin)
