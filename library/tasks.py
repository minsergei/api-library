import datetime
from datetime import timedelta
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from library.models import IssuanceBook


@shared_task
def send_email():
    """функция отправки писем пользователям о возврате книги"""
    books = IssuanceBook.objects.all()
    for item in books:
        print(datetime.datetime.now().date())
        if item.date_get + timedelta(days=13) == datetime.datetime.now().date():
            date = item.date_get+timedelta(days=14)
            send_mail(
                subject="Необходимо вернуть книгу",
                message=f'{item.user.email} вам необходимо вернуть книгу - {item.book.title} до {date}',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[item.user.email]
            )
