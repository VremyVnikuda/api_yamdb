import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from rest_framework.exceptions import ValidationError

from api_yamdb.settings import (CONFIRMATION_USER_LENGTH, DEFAULT_CODE,
                                NAME_MAX_LENGTH, TITLE_MAX_LENGTH)


class CommentsAndReviews(models.Model):
    """Комментарии Отзывы."""

    text = models.TextField('Текст',)
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:TITLE_MAX_LENGTH]


class CategoryAndGenre(models.Model):
    """Категория Жанр."""

    name = models.CharField('Название', max_length=NAME_MAX_LENGTH)
    slug = models.SlugField('Слаг', unique=True)

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name[:TITLE_MAX_LENGTH]


class User(AbstractUser):
    """Пользователи."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    USER_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )

    email = models.EmailField('Почта', unique=True)
    bio = models.TextField('Инфо', blank=True)
    role = models.CharField('Роль',
                            max_length=max(
                                [len(pos) for pos, _ in USER_CHOICES]),
                            choices=USER_CHOICES,
                            default=USER)
    confirmation_code = models.CharField('Код подтверждения',
                                         max_length=CONFIRMATION_USER_LENGTH,
                                         default=DEFAULT_CODE)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', )

    def clean(self):
        if self.username == 'me':
            raise ValidationError('Недопустимое имя пользователя')
        super().clean()

    @property
    def is_admin(self):
        return self.is_staff or self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR


class Category(CategoryAndGenre):
    """Категории."""

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(CategoryAndGenre):
    """Жанры."""

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Названия произведений."""

    name = models.CharField('Название', max_length=256)
    year = models.PositiveSmallIntegerField(
        'Год создания',
        validators=[MaxValueValidator(datetime.date.today().year,
                                      message='Год больше текущего')]
    )
    description = models.TextField('Описание', blank=True)
    genre = models.ManyToManyField(Genre)
    category = models.ForeignKey(Category,
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year',)
        default_related_name = 'titles'

    def __str__(self):
        return self.name[:TITLE_MAX_LENGTH]


class Review(CommentsAndReviews):
    """Отзывы."""

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField(
        'Оценка',
        validators=[MinValueValidator(1, message='Минимальное значение 1'),
                    MaxValueValidator(10, message='Максимальное значение 10')
                    ]
    )
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [models.UniqueConstraint(fields=['author', 'title'],
                                               name='unique_review')]
        default_related_name = 'reviews'


class Comment(CommentsAndReviews):
    """Комментарии."""

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор')
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               verbose_name='Отзыв')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
