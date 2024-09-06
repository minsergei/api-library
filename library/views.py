from django.db.models import Count
from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
import datetime

from library.models import Author, Book, IssuanceBook, StatisticIssuanceBook
from library.paginators import ResultsSetPagination
from library.serializers import AuthorSerializer, BookSerializer, IssuanceBookSerializer, \
    StatisticIssuanceBookSerializer
from users.permissions import IsManager


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    pagination_class = ResultsSetPagination

    def get_permissions(self):
        """Назначаем права на действия с авторами"""
        if self.action in ['update', 'destroy', 'create', 'partial_update']:
            self.permission_classes = (IsManager,)
        return super().get_permissions()


class BookCreateAPIView(generics.CreateAPIView):
    serializer_class = BookSerializer
    permission_classes = (IsManager,)


class BookListAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    pagination_class = ResultsSetPagination


class BookRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()


class BookUpdateAPIView(generics.UpdateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = (IsManager,)


class BookDestroyAPIView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = (IsManager,)


class IssuanceBookCreateAPIView(APIView):
    permission_classes = (IsManager,)
    queryset = [IssuanceBook.objects.all(), Book.objects.all()]
    serializer_class = IssuanceBookSerializer

    def post(self, *args, **kwargs):
        """Метод создания записи о выдаче книг, обновляет данные о наличии книги, создает запись в таблице статистики"""
        user = self.request.user
        book_id = self.request.data.get("book")
        book_item = get_object_or_404(Book, pk=book_id)
        book = Book.objects.get(id=book_id)
        subs_item, created = IssuanceBook.objects.get_or_create(user=user, book=book_item)

        if created:
            message = f'Вы выдали книгу {book.title} читателю {user.email}'
            status_code = status.HTTP_201_CREATED
            book.is_availability = False
            book.save(update_fields=["is_availability"])
        else:
            StatisticIssuanceBook.objects.create(user=user, book=book_item, date_get=subs_item.date_get)
            subs_item.delete()
            message = f'Вам вернули книгу {book.title} читатель {user.email}'
            status_code = status.HTTP_204_NO_CONTENT
            book.is_availability = True
            book.save(update_fields=["is_availability"])
        return Response({"message": message}, status=status_code)


class IssuanceBookListAPIView(generics.ListAPIView):
    serializer_class = IssuanceBookSerializer
    queryset = IssuanceBook.objects.all()


class StatisticIssuanceBookListAPIView(generics.ListAPIView):
    """
    эндпоинт для вывода статистики по книгам, которые чаще брали
    """
    serializer_class = StatisticIssuanceBookSerializer
    queryset = StatisticIssuanceBook.objects.values("book").annotate(total=Count("id")).order_by("-total")
