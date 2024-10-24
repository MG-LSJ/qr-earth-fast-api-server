from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "test"

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    FIXED_CODE: str
    ADMIN_PASSWORD: str

    # MAIL_USRNAME: str
    # MAIL_PASSWORD: str
    # MAIL_SERVER: str
    # MAIL_FROM_EMAIL: str
    # MAIL_FROM_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


Config = Settings()  # type: ignore
