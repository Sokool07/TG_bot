"""drop is_premium column

Revision ID: remove_is_premium_column
Revises: bd9b36fc385a
Create Date: 2024-10-18 00:00:00.000000

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "remove_is_premium_column"
down_revision: Union[str, None] = "bd9b36fc385a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column("users", "is_premium")


def downgrade() -> None:
    op.add_column(
        "users",
        sa.Column("is_premium", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.alter_column("users", "is_premium", server_default=None)
