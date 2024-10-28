# QR Earth Server

Written in Python's Fast Api & SQLModel (with SQLAlchemy 2.0). Uses PostgreSQL
for database and Redis for caching. Currently deployed on azure

api docs: https://qr-earth-bthhbwfcbxcvfrbp.eastus-01.azurewebsites.net/docs

### Environemnt variables required to run:

```py
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
```
