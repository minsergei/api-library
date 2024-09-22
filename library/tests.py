from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Author, Book
from users.models import User


class LibraryTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            email="serg@mail.ru",
            is_staff=True,
            is_active=True,
            is_superuser=False
        )
        self.user.set_password('test_user')
        self.user.save()

        self.client.force_authenticate(user=self.user)

        self.author = Author.objects.create(
            fio='test_place',
            biography='test_action',
        )

    def test_create_author(self):
        """Тестирование создания автора"""

        data = {
            "fio": "Пушкин АС",
            "biography": "Родился в 1878 году"
        }

        response = self.client.post('/author/', data=data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Author.objects.all().count(), 2)

    def test_create_book(self):
        """Тестирование создания книги"""

        data = {
            "title": "Герой нашего времени",
            "description": "Про героя",
            "genre": "novel",
            "date": "1810-09-05",

        }

        response = self.client.post('/book/create/', data=data)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(Book.objects.all().count(), 1)
