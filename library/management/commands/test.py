# from django.db.models import Count
#
# from library.models import StatisticIssuanceBook
#

import smtplib
from datetime import datetime, timedelta

from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail
from django.core.cache import cache

from django.core.management import BaseCommand
from django.db.models import Count

from library.models import StatisticIssuanceBook


class Command(BaseCommand):

    def handle(self, *args, **options):
        queryset = StatisticIssuanceBook.objects.values("book").annotate(total=Count("id"))
        print(queryset)