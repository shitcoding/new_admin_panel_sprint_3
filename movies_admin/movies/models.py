import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class CreatedMixin(models.Model):
    created = models.DateTimeField(_('created'), auto_now_add=True)

    class Meta:
        abstract = True


class ModifiedMixin(models.Model):
    modified = models.DateTimeField(_('modified'), auto_now=True)

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class Genre(UUIDMixin, CreatedMixin, ModifiedMixin):
    name = models.CharField(_('name'), max_length=255, null=False)
    description = models.TextField(_('description'), blank=True)

    class Meta:
        # fmt: off
        db_table = "content\".\"genre"
        # fmt: on
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.name


class FilmworkType(models.TextChoices):
    MOVIE = 'movie', _('movie')
    TV_SHOW = 'tv_show', _('TV show')


class GenreFilmwork(UUIDMixin, CreatedMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

    class Meta:
        # fmt: off
        db_table = "content\".\"genre_film_work"
        # fmt: on

        constraints = [
            models.UniqueConstraint(
                fields=['genre', 'film_work'],
                name='genre_film_work_unique_idx',
            )
        ]

        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')

    def __str__(self):
        return self.genre.name


class Person(UUIDMixin, CreatedMixin, ModifiedMixin):
    full_name = models.CharField(_('full name'), max_length=255, null=False)

    class Meta:
        # fmt: off
        db_table = "content\".\"person"
        # fmt: on
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return self.full_name


class RoleType(models.TextChoices):
    ACTOR = 'actor', _('Actor')
    DIRECTOR = 'director', _('Director')
    WRITER = 'writer', _('Writer')
    PRODUCER = 'producer', _('Producer')
    COMPOSER = 'composer', _('Composer')
    CINEMATOGRAPHER = 'cinematographer', _('Cinematographer')
    EDITOR = 'editor', _('Editor')


class PersonFilmwork(UUIDMixin, CreatedMixin):
    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.CharField(_('role'), max_length=25, choices=RoleType.choices)

    class Meta:
        # fmt: off
        db_table = "content\".\"person_film_work"
        # fmt: on

        constraints = [
            models.UniqueConstraint(
                fields=['film_work', 'person', 'role'],
                name='film_work_person_role_idx',
            )
        ]

        verbose_name = _('Person')
        verbose_name_plural = _('Persons')

    def __str__(self):
        return f'{self.person.full_name}: {self.role}'


class Filmwork(UUIDMixin, CreatedMixin, ModifiedMixin):
    title = models.CharField(_('name'), max_length=255, null=False)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation date'))
    rating = models.FloatField(
        _('rating'),
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    type = models.CharField(
        _('type'),
        max_length=10,
        choices=FilmworkType.choices,
        null=False,
    )
    file_path = models.CharField(
        _('file path'), max_length=255, null=True, blank=True
    )
    genres = models.ManyToManyField(
        Genre, through=GenreFilmwork, related_name='film_works'
    )
    persons = models.ManyToManyField(
        Person, through=PersonFilmwork, related_name='film_works'
    )

    class Meta:
        # fmt: off
        db_table = "content\".\"film_work"
        # fmt: on

        indexes = [
            models.Index(
                fields=['creation_date'], name='film_work_creation_date_idx'
            )
        ]

        verbose_name = _('Filmwork')
        verbose_name_plural = _('Filmworks')

    def __str__(self):
        return self.title
