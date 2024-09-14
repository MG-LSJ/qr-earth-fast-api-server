QR Earth Server

Written in Python's Fast Api & SQLModel (with SQLAlchemy 2.0).
Currently deployed on azure

Environemnt variables required to run:

```py
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "password"
    DB_NAME: str = "test"

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"

    FIXED_CODE: str
    ADMIN_PASSWORD: str
```
