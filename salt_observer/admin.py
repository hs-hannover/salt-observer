from django.contrib import admin

from salt_observer.models import (
    Minion, Network, NetworkInterface, Domain
)


class NetworkInterfaceInline(admin.TabularInline):
    model = NetworkInterface
    extra = 0
    readonly_fields = ('network', 'minion', 'mac_address', 'name')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class MinionAdmin(admin.ModelAdmin):
    inlines = [NetworkInterfaceInline]
    readonly_fields = ('fqdn', 'data', 'last_updated')
    exclude = ('_data',)
admin.site.register(Minion, MinionAdmin)


class NetworkAdmin(admin.ModelAdmin):
    inlines = [NetworkInterfaceInline]
    readonly_fields = ('ipv4', 'mask', 'last_updated')
admin.site.register(Network, NetworkAdmin)


class DomainAdmin(admin.ModelAdmin):
    list_display = ('fqdn', 'minion_count', 'public', 'can_speak_https')
    filter_horizontal = ('minion',)
admin.site.register(Domain, DomainAdmin)
