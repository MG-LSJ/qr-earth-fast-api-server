"""init

Revision ID: b99ab3db54f1
Revises: 
Create Date: 2024-10-24 18:41:55.534922

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b99ab3db54f1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("phone_number", sqlmodel.sql.sqltypes.AutoString(), nullable=True),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("username", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column(
            "hashed_password", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.Column("full_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("redeemed_code_count", sa.Integer(), nullable=False),
        sa.Column("points", sa.Integer(), nullable=False),
        sa.Column("deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "codes",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("value", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=True),
        sa.Column("redeemed", sa.Boolean(), nullable=False),
        sa.Column("redeemed_at", postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "transaction",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("timestamp", postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("transaction")
    op.drop_table("codes")
    op.drop_table("users")
    # ### end Alembic commands ###
