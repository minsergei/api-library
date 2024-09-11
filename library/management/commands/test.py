from django.core.management import BaseCommand
from django.db.models import Count

from library.models import StatisticIssuanceBook


class Command(BaseCommand):

    def handle(self, *args, **options):
        queryset = StatisticIssuanceBook.objects.values("book").annotate(total=Count("id"))
        print(queryset)
