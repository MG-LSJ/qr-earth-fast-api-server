from sqlmodel import SQLModel


class UserLeaderboard(SQLModel, table=False):
    username: str
    redeemed_code_count: int
