from django.core.management.base import BaseCommand

from salt_observer.models import Domain


class Command(BaseCommand):
    help = 'Check all domains if they are valid'

    def handle(self, *args, **kwargs):
        ''' Check every domain '''

        for domain in Domain.objects.all():
            domain.check_if_valid()
