from django.contrib import admin
from library.models import Book, Author, IssuanceBook


@admin.register(Book)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "title",)


@admin.register(Author)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "fio",)


@admin.register(IssuanceBook)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "book", "date")
