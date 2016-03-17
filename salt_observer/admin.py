from django.contrib import admin

from salt_observer.models import Minion, Network, NetworkInterface


class NetworkInterfaceInline(admin.TabularInline):
    model = NetworkInterface
    extra = 0
    readonly_fields = ('network', 'minion', 'mac_address')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class MinionAdmin(admin.ModelAdmin):
    inlines = [NetworkInterfaceInline]
    readonly_fields = ('fqdn', 'grains',)
admin.site.register(Minion, MinionAdmin)


class NetworkAdmin(admin.ModelAdmin):
    inlines = [NetworkInterfaceInline]
    readonly_fields = ('ipv4', 'mask')
admin.site.register(Network, NetworkAdmin)
