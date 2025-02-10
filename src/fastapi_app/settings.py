from pydantic_settings import BaseSettings as PydanticBaseSettings, SettingsConfigDict


class BaseSettings(PydanticBaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra='ignore'
    )


class Settings(BaseSettings):
    SECRET_KEY: str
    JWT_ALGORITHM: str


Config = Settings()
