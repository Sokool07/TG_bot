"""merge heads

Revision ID: 1ff46664e795
Revises: e4b7e8c165c1, remove_is_premium_column
Create Date: 2025-09-18 06:48:12.914379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ff46664e795'
down_revision: Union[str, None] = ('e4b7e8c165c1', 'remove_is_premium_column')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
