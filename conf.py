import functools

import mongoengine
import pydantic


class MongodbDNS(pydantic.AnyUrl):
    allowed_schemes = {'mongodb', 'mongodb+srv', 'mongomock'}


class SettingsBase(pydantic.BaseSettings):
    ENVIRONMENT: str = 'dev'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class Settings(SettingsBase):
    MONGODB_URL: MongodbDNS = 'mongodb://localhost/simpals_test'
    SECRET_KEY: str = 'hQmr6Hc!itcvj2%Z+~BvFS?ySQkNg8|?@4D}2Kk2eM2BaB@uLO?@Z)/a{yD_YM0'

    API_KEY: str = ''
    API_USERNAME: str = ''
    API_PASS: str = ''
    API_URL: str = ''


class DevSettings(Settings):
    pass


class StageSettings(Settings):
    pass


class ProdSettings(Settings):
    pass


class SettingsTest(Settings):
    MONGODB_URL: MongodbDNS = 'mongomock://localhost'

    class Config:
        # We don't want tests to use env variables/files
        env_file = None
        env_file_encoding = 'utf-8'


@functools.cache
def get_settings() -> Settings:
    # https://rednafi.github.io/digressions/python/2020/06/03/python-configs.html
    environment = SettingsBase().ENVIRONMENT

    settings_class = {
        'dev': DevSettings,
        'stage': StageSettings,
        'prod': ProdSettings,
        'testing': SettingsTest,
    }.get(environment.lower())

    if not settings_class:
        raise RuntimeError(f'Invalid ENVIRONMENT: {environment!r}')

    settings = settings_class()

    mongoengine.register_connection(mongoengine.DEFAULT_CONNECTION_NAME, host=settings.MONGODB_URL)

    return settings
