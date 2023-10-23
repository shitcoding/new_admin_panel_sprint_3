from rest_framework import serializers

from movies.models import Filmwork


class FilmworkSerializer(serializers.ModelSerializer):
    genres = serializers.ReadOnlyField(source='annotated_genres')
    actors = serializers.ReadOnlyField(source='annotated_actors')
    directors = serializers.ReadOnlyField(source='annotated_directors')
    writers = serializers.ReadOnlyField(source='annotated_writers')

    class Meta:
        model = Filmwork
        fields = (
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type',
            'genres',
            'actors',
            'directors',
            'writers',
        )
