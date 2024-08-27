from sqlmodel import SQLModel


class UserLeaderboard(SQLModel, table=False):
    username: str
    points: int
