import os
from typing import List, Optional

from pydantic.env_settings import BaseSettings
from pydantic.fields import Field


class Postgres(BaseSettings):
    host: str = Field('127.0.0.1', env='POSTGRES_HOST')
    port: int = Field(5432, env='POSTGRES_PORT')
    user: str = Field('delivery', env='POSTGRES_USER')
    password: str = Field('delivery', env='POSTGRES_PASSWORD')
    database: str = Field('delivery', env='POSTGRES_DB')

    @property
    def uri(self) -> str:
        return f'postgres://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'

    def dict(
        self,
        *,
        include=None,
        exclude=None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ):
        d = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        if isinstance(d, dict):
            d['uri'] = self.uri
        return d


class Connections(BaseSettings):
    @property
    def default(self) -> str:
        postgres = Postgres()
        return postgres.uri

    def dict(
        self,
        *,
        include=None,
        exclude=None,
        by_alias: bool = False,
        skip_defaults: Optional[bool] = None,
        exclude_unset: bool = False,
        exclude_defaults: bool = False,
        exclude_none: bool = False,
    ):
        d = super().dict(
            include=include,
            exclude=exclude,
            by_alias=by_alias,
            skip_defaults=skip_defaults,
            exclude_defaults=exclude_defaults,
            exclude_none=exclude_none,
        )
        if isinstance(d, dict):
            d['default'] = self.default
        return d


class Versions(BaseSettings):
    models: List[str] = [
        'app.models',
        'aerich.models',
    ]
    default_connection: str = 'default'


class Apps(BaseSettings):
    versions: Versions = Versions()


class Tortoise(BaseSettings):
    connections: Connections = Connections()
    apps: Apps = Apps()
    use_tz: bool = False


class Settings(BaseSettings):
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "test_key")
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    POSTGRES: Postgres = Postgres()
    TORTOISE: Tortoise = Tortoise()

    class Config:
        case_sensitive = False


settings = Settings()
tortoise_orm = settings.dict()['TORTOISE']
