"""empty message

Revision ID: m2_merge
Revises: a2_featured, b2_description
Create Date: 2025-12-25 15:45:27.084936

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'm2_merge'
down_revision: Union[str, Sequence[str], None] = ('a2_featured',
                                                  'b2_description')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
