from django.contrib import admin

from salt_observer.models import Minion


class MinionAdmin(admin.ModelAdmin):
    readonly_fields = ('grains',)
admin.site.register(Minion, MinionAdmin)
