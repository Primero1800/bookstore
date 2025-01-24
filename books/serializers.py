from rest_framework import serializers

from books.models import AuthorAdsSettings


class AuthorAdsSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthorAdsSettings
        fields = (
            'id',
            'author',
            'url',
            'settings',
            'crontab',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('author', 'id',)