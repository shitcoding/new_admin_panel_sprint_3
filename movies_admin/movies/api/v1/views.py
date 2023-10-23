from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from rest_framework import generics

from movies.api.v1.pagination import Paginator
from movies.api.v1.serializers import FilmworkSerializer
from movies.models import Filmwork


class MoviesDetailApi(generics.RetrieveAPIView):
    queryset = Filmwork.objects.all()
    serializer_class = FilmworkSerializer

    def get_object(self):
        return (
            self.queryset.prefetch_related('genres', 'persons')
            .annotate(
                annotated_genres=ArrayAgg('genres__name', distinct=True),
                annotated_actors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role='actor'),
                    distinct=True,
                ),
                annotated_directors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role='director'),
                    distinct=True,
                ),
                annotated_writers=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role='writer'),
                    distinct=True,
                ),
            )
            .get(pk=self.kwargs['pk'])
        )


class MoviesListApi(generics.ListAPIView):
    serializer_class = FilmworkSerializer
    pagination_class = Paginator

    def get_queryset(self):
        return (
            Filmwork.objects.all()
            .prefetch_related('genres', 'persons')
            .annotate(
                annotated_genres=ArrayAgg('genres__name', distinct=True),
                annotated_actors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role='actor'),
                    distinct=True,
                ),
                annotated_directors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role='director'),
                    distinct=True,
                ),
                annotated_writers=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role='writer'),
                    distinct=True,
                ),
            )
        )
