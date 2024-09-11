from rest_framework import serializers
from library.models import Book, Author, IssuanceBook, StatisticIssuanceBook


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('__all__')


class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('__all__')


class IssuanceBookSerializer(serializers.ModelSerializer):

    class Meta:
        model = IssuanceBook
        fields = ('__all__')


class StatisticIssuanceBookSerializer(serializers.ModelSerializer):
    """
    серилайзер для вывода статистики по книгам, которые чаще брали
    """
    total = serializers.SerializerMethodField()
    book = serializers.SerializerMethodField()

    class Meta:
        model = StatisticIssuanceBook
        fields = ('book', "total",)

    def get_total(self, obj):
        return obj['total']

    def get_book(self, obj):
        return obj['book']
