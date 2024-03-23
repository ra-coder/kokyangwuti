from pathlib import Path

from celery import Celery
from dotenv import load_dotenv
from pydantic import RedisDsn
from pydantic_settings import BaseSettings
from starlette.staticfiles import StaticFiles


class Config(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent

    # AWS
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_ENDPOINT_URL: str = 'https://storage.yandexcloud.net'
    AWS_S3_REGION_NAME: str = 'storage'

    # CELERY
    CELERY_BROKER_URL: RedisDsn
    CELERY_RESULT_BACKEND: RedisDsn


load_dotenv()
settings = Config()

celery = Celery()
celery.config_from_object(obj=settings, namespace="CELERY")
celery.autodiscover_tasks(packages=["src"])
