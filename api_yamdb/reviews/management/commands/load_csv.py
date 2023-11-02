from django.apps import apps
from django.core.management.base import BaseCommand

from reviews.management.commands.utils import (comment_loader, csv_loader,
                                               review_loader, title_loader)
from reviews.models import Category, Genre, User


CONSOLE_STRING_LENGTH = 70


class Command(BaseCommand):
    """Загрузка из csv файлов."""

    def handle(self, **options):
        err = 0
        err = csv_loader(User, 'static/data/users.csv') + err
        err = csv_loader(Category, 'static/data/category.csv') + err
        err = csv_loader(Genre, 'static/data/genre.csv') + err
        err = title_loader('static/data/titles.csv') + err
        err = csv_loader(apps.get_model('reviews', 'title_genre'),
                         'static/data/genre_title.csv') + err
        err = review_loader('static/data/review.csv') + err
        err = comment_loader('static/data/comments.csv') + err

        if err:
            print(f'\n Ошибок загруки :{err}')
        else:
            print('\n Загрузка завершена, ошибок нет')
