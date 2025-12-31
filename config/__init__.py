try:
    from .celery import app as celery_app
    __all__ = ("celery_app",)
except ModuleNotFoundError:
    # اگر celery نصب نبود یا با python اشتباه اجرا شد، پروژه نخوابه
    celery_app = None
    __all__ = ()
