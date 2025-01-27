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
        read_only_fields = ('id', )

    def validate_settings(self, value):
        if not isinstance(value, dict) or not 'crontab' in value:
            raise serializers.ValidationError('Settings must be in dictionary type and consist of \'crontab\' key')
        if len(value['crontab'].split(' ')) != 5:
            raise serializers.ValidationError('\'Crontab\' must have 5 parts exactly')
        return value
