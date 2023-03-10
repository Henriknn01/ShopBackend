from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group


class Command(BaseCommand):
    help = 'Create the four groups'

    def handle(self, *args, **options):
        Group.objects.create(name='user')
        Group.objects.create(name='support')
        Group.objects.create(name='sale')
        Group.objects.create(name='admin')


