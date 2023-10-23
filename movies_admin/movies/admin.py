from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Filmwork, Genre, GenreFilmwork, Person, PersonFilmwork


class GenreFilmworkInline(admin.TabularInline):
    model = GenreFilmwork
    extra = 0
    verbose_name = _('Genre')
    verbose_name_plural = _('Genres')
    autocomplete_fields = ('genre',)


class PersonFilmworkInline(admin.TabularInline):
    model = PersonFilmwork
    extra = 0
    verbose_name = _('Person')
    verbose_name_plural = _('Persons')
    autocomplete_fields = ('person',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'get_films_count',
        'modified',
    )

    search_fields = ('name',)

    def get_queryset(self, request):
        queryset = (
            super(GenreAdmin, self)
            .get_queryset(request)
            .prefetch_related('film_works')
        )
        return queryset

    def get_films_count(self, obj):
        return obj.film_works.count()

    get_films_count.short_description = _('Total')


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        'full_name',
        'modified',
    )

    search_fields = ('full_name',)
    ordering = ('full_name',)


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    inlines = (
        GenreFilmworkInline,
        PersonFilmworkInline,
    )

    autocomplete_fields = ('persons',)

    list_display = (
        'title',
        'type',
        'creation_date',
        'rating',
        'get_genres',
        'created',
        'modified',
    )

    list_prefetch_related = ('genres',)

    list_filter = ('type',)

    search_fields = (
        'title',
        'description',
        'id',
    )

    def get_queryset(self, request):
        queryset = (
            super()
            .get_queryset(request)
            .prefetch_related(*self.list_prefetch_related)
        )
        return queryset

    def get_genres(self, obj):
        return ', '.join([genre.name for genre in obj.genres.all()])

    get_genres.short_description = _('Genres')
