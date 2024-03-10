from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_S3_ENDPOINT_URL: str = 'https://storage.yandexcloud.net'
    AWS_S3_REGION_NAME: str = 'storage'


settings = Settings()
