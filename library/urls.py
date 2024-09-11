from django.urls import path
from rest_framework.routers import DefaultRouter
from library.apps import LibraryConfig
from library.views import (
    AuthorViewSet,
    BookListAPIView,
    BookCreateAPIView,
    BookRetrieveAPIView,
    BookUpdateAPIView,
    BookDestroyAPIView,
    IssuanceBookCreateAPIView,
    IssuanceBookListAPIView,
    StatisticIssuanceBookListAPIView,
    BookListAPIViewActive,
)

app_name = LibraryConfig.name

router = DefaultRouter()
router.register(r"author", AuthorViewSet, basename="authors")

urlpatterns = [
    path("books/", BookListAPIView.as_view(), name="books_list"),
    path("books/is_availability/", BookListAPIViewActive.as_view(), name="books_list_is_availability"),
    path("book/create/", BookCreateAPIView.as_view(), name="book_create"),
    path("book/<int:pk>/", BookRetrieveAPIView.as_view(), name="book_detail"),
    path("book/update/<int:pk>/", BookUpdateAPIView.as_view(), name="book_update"),
    path("book/delete/<int:pk>/", BookDestroyAPIView.as_view(), name="book_delete"),
    path("issuance/", IssuanceBookCreateAPIView.as_view(), name="issuance_book"),
    path(
        "issuance_list/", IssuanceBookListAPIView.as_view(), name="issuance_book_list"
    ),
    path("statistic/", StatisticIssuanceBookListAPIView.as_view(), name="statistic"),
] + router.urls
