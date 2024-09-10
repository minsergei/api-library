from django.db.models import Count

from rest_framework import viewsets, generics, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404

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
    """Все книги библиотеки"""
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    pagination_class = ResultsSetPagination
    filter_backends = [SearchFilter,]
    search_fields = ['title', 'genre', 'author__fio']


class BookListAPIViewActive(generics.ListAPIView):
    """Список книг в наличии"""
    serializer_class = BookSerializer
    queryset = Book.objects.filter(is_availability=True)
    pagination_class = ResultsSetPagination
    filter_backends = [SearchFilter,]
    search_fields = ['title', 'genre', 'author__fio']


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
    permission_classes = (IsAuthenticated,)
    queryset = [IssuanceBook.objects.all(), Book.objects.all()]
    serializer_class = IssuanceBookSerializer

    def post(self, *args, **kwargs):
        """
        Метод создания записи о выдаче книг, обновляет данные о наличии книги, создает запись в таблице статистики.
        Если книга выдана, то выведется сообщение, что книга у другого пользователя.
        Для запроса необходимо указать ID книги из списка книг в наличии.
        """
        user = self.request.user
        book_id = self.request.data.get("book")
        book_item = get_object_or_404(Book, pk=book_id)
        book = Book.objects.get(id=book_id)
        issuance = IssuanceBook.objects.filter(book=book_id)
        if issuance.count() == 1:
            if user != issuance[0].user:
                message = f'В данный момент книга {book.title} на руках'
                status_code = status.HTTP_204_NO_CONTENT
                return Response({"message": message}, status=status_code)
            else:
                subs_item, created = IssuanceBook.objects.get_or_create(user=user, book=book_item)
                if created:
                    message = f'Вам выдали книгу {book.title}, читателю {user.email}'
                    status_code = status.HTTP_201_CREATED
                    book.is_availability = False
                    book.save(update_fields=["is_availability"])
                else:
                    StatisticIssuanceBook.objects.create(user=user, book=book_item, date_get=subs_item.date_get)
                    subs_item.delete()
                    message = f'Вы вернули книгу {book.title}, читатель {user.email}'
                    status_code = status.HTTP_204_NO_CONTENT
                    book.is_availability = True
                    book.save(update_fields=["is_availability"])
                return Response({"message": message}, status=status_code)
        else:
            IssuanceBook.objects.create(user=user, book=book_item)
            message = f'Вам выдали книгу {book.title}, читателю {user.email}'
            status_code = status.HTTP_201_CREATED
            book.is_availability = False
            book.save(update_fields=["is_availability"])
            return Response({"message": message}, status=status_code)


class IssuanceBookListAPIView(generics.ListAPIView):
    """
    Представления для вывода книг, которые выданы пользователям
    """
    serializer_class = IssuanceBookSerializer
    queryset = IssuanceBook.objects.all()
    permission_classes = (IsManager,)


class StatisticIssuanceBookListAPIView(generics.ListAPIView):
    """
    Представления для вывода статистики по книгам, которые чаще брали
    """
    serializer_class = StatisticIssuanceBookSerializer
    queryset = StatisticIssuanceBook.objects.values("book").annotate(total=Count("id")).order_by("-total")
    permission_classes = (IsManager,)
