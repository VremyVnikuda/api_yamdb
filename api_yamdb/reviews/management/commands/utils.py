import csv

from django.shortcuts import get_object_or_404

from reviews.admin import User
from reviews.models import Category, Comment, Review, Title

CONSOLE_STRING_LENGTH = 70


def csv_loader(table_name, file_name):
    table_name.objects.all().delete()
    errors_count = 0
    print(f'{file_name}'[:CONSOLE_STRING_LENGTH])
    with open(file_name, encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(f'{row}'[:CONSOLE_STRING_LENGTH])
            try:
                table_name.objects.get_or_create(**row)
            except Exception as err:
                print(f'Ошибка загрузки {err}'[:CONSOLE_STRING_LENGTH])
                errors_count = errors_count + 1
    return errors_count


def title_loader(file_name):
    err = 0
    Title.objects.all().delete()
    print('Загрузка наименований')
    with open(file_name, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            print(f'{row}'[:CONSOLE_STRING_LENGTH])
            try:
                category = get_object_or_404(Category, pk=row[3])
                Title.objects.get_or_create(id=row[0],
                                            name=row[1],
                                            year=row[2],
                                            category=category)
            except Exception as err:
                print(f'Ошибка загрузки {err}'[:CONSOLE_STRING_LENGTH])
                print(f'Category={category}'[:CONSOLE_STRING_LENGTH])
                err = err + 1

    return err


def review_loader(file_name):
    err = 0
    Review.objects.all().delete()
    print('Загрузка отзывов')
    with open(file_name, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            print(f'{row}'[:CONSOLE_STRING_LENGTH])
            try:
                Review.objects.get_or_create(
                    id=row[0],
                    title=get_object_or_404(Title, pk=row[1]),
                    text=row[2],
                    author=get_object_or_404(User, pk=row[3]),
                    score=row[4],
                    pub_date=row[5],
                )
            except Exception as err:
                print(f'Ошибка {err}')
                err = err + 1
    return err


def comment_loader(file_name):
    err = 0
    Comment.objects.all().delete()
    print('Загрузка комментариев')
    with open(file_name, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            print(f'{row}'[:CONSOLE_STRING_LENGTH])
            try:
                Comment.objects.get_or_create(
                    id=row[0],
                    review=get_object_or_404(Review, pk=row[1]),
                    text=row[2],
                    author=get_object_or_404(User, pk=row[3]),
                    pub_date=row[4],
                )
            except Exception as err:
                print(f'Ошибка {err}')
                err = err + 1
    return err
