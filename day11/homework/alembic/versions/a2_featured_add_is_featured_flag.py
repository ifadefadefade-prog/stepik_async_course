"""Add is_featured flag

Revision ID: a2_featured
Revises: 006
Create Date: 2025-12-25 15:04:30.950184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a2_featured'
down_revision: Union[str, Sequence[str], None] = '006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('products', sa.Column('is_featured', sa.Boolean(),
                                        server_default=sa.text('false'),
                                        nullable=False))


def downgrade() -> None:
    op.drop_column('products', 'is_featured')
