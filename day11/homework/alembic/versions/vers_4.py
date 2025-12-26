from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '004'
down_revision: Union[str, Sequence[str], None] = '003'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    product_status_enum = sa.Enum(
        'draft',
        'published',
        'archived',
        name='product_status'
    )
    product_status_enum.create(op.get_bind(), checkfirst=True)

    op.add_column('products',
                  sa.Column('status', product_status_enum,
                            nullable=False, server_default='draft'))


def downgrade() -> None:
    op.drop_column('products', 'status')

    product_status_enum = sa.Enum(
        'draft',
        'published',
        'archived',
        name='product_status'
    )
    product_status_enum.drop(op.get_bind(), checkfirst=True)
