import os
from celery import Celery
from celery.schedules import crontab # type: ignore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "release-expired-reservations-every-minute": {
        "task": "inventory.tasks.release_expired_reservations",
        "schedule": crontab(minute="*/1"),
        "args": (200,),
    }
}
