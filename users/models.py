from django.db import models
from django.contrib.auth.models import AbstractUser

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="email", unique=True)
    avatar = models.ImageField(
        upload_to="media/users/",
        verbose_name="Аватар",
        help_text="Укажите аватар",
        **NULLABLE
    )
    telephone = models.CharField(
        max_length=35,
        verbose_name="телефон",
        help_text="Введите телефон",
        **NULLABLE
    )
    city = models.CharField(
        max_length=35,
        verbose_name="город",
        help_text="Введите город",
        **NULLABLE
    )
    token = models.CharField(
        max_length=50,
        verbose_name="токен",
        **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email}"
