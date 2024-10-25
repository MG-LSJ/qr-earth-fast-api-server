from sqlmodel import SQLModel


class AdminLogin(SQLModel):
    password: str
