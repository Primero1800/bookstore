import json
from typing import Any

from django_celery_beat.models import CrontabSchedule, PeriodicTask

from books.models import AuthorAdsSettings
from books.serializers import AuthorAdsSettingsSerializer


def create_author_ads_settings(validated_data: dict[str, Any]) -> AuthorAdsSettings | None:
    """Создание нового экземпляра AuthorAdsSettings (настроек рекламы пользователя)
    В том числе создаются задания для Celery
    """
    settings = AuthorAdsSettings.objects.create(**validated_data)

    try:
        minute, hour, day_of_week, day_of_month, month_of_year = settings.settings['crontab'].split(' ')
    except ValueError:
        return None

    crontab_schedule, _ = CrontabSchedule.objects.get_or_create(
        minute=minute,
        hour=hour,
        day_of_week=day_of_week,
        day_of_month=day_of_month,
        month_of_year=month_of_year,
    )

    periodic_task = PeriodicTask.objects.create(
        crontab=crontab_schedule,
        name=f"Author Ads Settings {settings.id}",
        task='books.tasks.clicked',
        args=json.dumps([str(settings.author), settings.url]),
    )

    settings.crontab = periodic_task
    settings.save()

    return settings
