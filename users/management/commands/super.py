from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        u = User.objects.create(email='admin@admin.ru', is_superuser=True, is_staff=True)
        u.set_password("123qwe")
        u.save()
