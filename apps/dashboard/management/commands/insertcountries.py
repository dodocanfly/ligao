from django.core.management.base import BaseCommand
from ._private import insert_countries


class Command(BaseCommand):
    help = 'Insert countries to db'

    def handle(self, *args, **options):
        data = insert_countries()
        self.stdout.write(self.style.SUCCESS(f"Succesfull! existed: {data[0]}, created: {data[1]}"))
