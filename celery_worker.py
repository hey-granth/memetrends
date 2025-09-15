from memetrends import app as celery_app
from os import environ


environ.setdefault("DJANGO_SETTINGS_MODULE", "memetrends.settings")

if __name__ == "__main__":
    celery_app.start()
