from django.db import models
from config import settings

NULLABLE = {"blank": True, "null": True}


class Book(models.Model):
    title = models.CharField(
        max_length=150,
        verbose_name="название книги",
        help_text="Укажите название книги",
    )
    preview = models.ImageField(
        upload_to="media/library/book",
        verbose_name="обложка книги",
        help_text="Добавьте превью изображения",
        **NULLABLE,
    )
    description = models.TextField(
        verbose_name="описание книги", help_text="Укажите описание книги"
    )
    author = models.ForeignKey(
        "Author",
        on_delete=models.SET_NULL,
        **NULLABLE,
        verbose_name="Автор книги",
    )
    GENRE_FANTASY = "fantasy"
    GENRE_NOVEL = "novel"
    GENRE_DETECTIVE = "detective"
    GENRE_CLASSIC = "classic"
    GENRE_FAIRY_TALE = "fairy tale"
    GENRE_CHOICES = (
        (GENRE_FANTASY, "фэнтези"),
        (GENRE_NOVEL, "роман"),
        (GENRE_DETECTIVE, "детектив"),
        (GENRE_CLASSIC, "классическая литература"),
        (GENRE_FAIRY_TALE, "сказка"),
    )
    genre = models.CharField(
        max_length=50, choices=GENRE_CHOICES, verbose_name="жанр книги", **NULLABLE
    )
    date = models.DateField(
        **NULLABLE,
        verbose_name="Дата выхода книги",
        help_text="Формат DD.MM.YYYY",
    )
    is_availability = models.BooleanField(default=True, verbose_name="Наличие книги")

    def __str__(self):
        return f"{self.author} - {self.title}"

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class Author(models.Model):
    fio = models.CharField(
        max_length=150,
        verbose_name="ФИО автора",
        help_text="Укажите ФИО автора",
    )
    biography = models.TextField(
        **NULLABLE,
        verbose_name="биография автора",
        help_text="Укажите биографию автора",
    )

    def __str__(self):
        return f"{self.fio}"

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class IssuanceBook(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    date_get = models.DateField(
        auto_now_add=True,
        verbose_name="Дата выдача книги",
        help_text="Формат DD.MM.YYYY",
    )


class StatisticIssuanceBook(models.Model):
    user = models.EmailField(verbose_name="email")
    book = models.CharField(
        max_length=150,
        verbose_name="название книги",
        help_text="Укажите название книги",
    )
    date_get = models.DateField(
        verbose_name="Дата выдача книги",
        help_text="Формат DD.MM.YYYY",
    )
    date_return = models.DateField(
        auto_now_add=True,
        verbose_name="Дата возврата книги",
        help_text="Формат DD.MM.YYYY",
    )

    def __str__(self):
        return f"Книга {self.book} выдана пользователю {self.user}"

    class Meta:
        verbose_name = "статистика книг"
        verbose_name_plural = "статистика книг"
