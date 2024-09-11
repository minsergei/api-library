# Generated by Django 4.2 on 2024-09-06 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0003_remove_issuancebook_date_issuancebook_date_get_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="StatisticIssuanceBook",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user", models.EmailField(max_length=254, verbose_name="email")),
                (
                    "book",
                    models.CharField(
                        help_text="Укажите название книги",
                        max_length=150,
                        verbose_name="название книги",
                    ),
                ),
                (
                    "date_get",
                    models.DateField(
                        help_text="Формат DD.MM.YYYY", verbose_name="Дата выдача книги"
                    ),
                ),
                (
                    "date_return",
                    models.DateField(
                        auto_now_add=True,
                        help_text="Формат DD.MM.YYYY",
                        verbose_name="Дата возврата книги",
                    ),
                ),
            ],
            options={
                "verbose_name": "статистика книг",
                "verbose_name_plural": "статистика книг",
            },
        ),
        migrations.AlterModelOptions(
            name="issuancebook",
            options={},
        ),
        migrations.RemoveField(
            model_name="issuancebook",
            name="date_return",
        ),
    ]
