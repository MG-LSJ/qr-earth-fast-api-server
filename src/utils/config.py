from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "test"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "password"

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    HASHED_ADMIN_PASSWORD: str

    ORIGINS: list[str]
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


Config = Settings()  # type: ignore
