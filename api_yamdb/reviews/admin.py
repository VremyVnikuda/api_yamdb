from django.contrib import admin
from django.contrib.auth import get_user_model

from reviews.models import Review, Comment, Title, Category, Genre

User = get_user_model()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'get_genres',
                    'description', 'category')
    list_filter = ('category',)
    list_editable = ('category', )

    def get_genres(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])

    get_genres.short_description = 'Жанры'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'score', 'pub_date', 'title')
    search_fields = ('title', 'text')
    list_filter = ('pub_date', 'score')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date', 'review')
    search_fields = ('review', 'text')
    list_filter = ('pub_date',)


@admin.register(User)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'date_joined', 'role', 'is_active')
    search_fields = ('username', 'email')
    list_editable = ('is_active', 'role', )
    list_filter = ('role', 'is_active')
