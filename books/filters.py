from django_filters import FilterSet

from books.models import AuthorAdsSettings

class AuthorAdsSettingsFilterSet(FilterSet):
    class Meta:
        model = AuthorAdsSettings
        fields = {
            'author': ['exact',],
            'crontab': ['exact', ],
        }