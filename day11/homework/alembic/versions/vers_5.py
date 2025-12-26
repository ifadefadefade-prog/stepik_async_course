from typing import Sequence, Union

from alembic import op


revision: str = '005'
down_revision: Union[str, Sequence[str], None] = '004'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        "ALTER TYPE product_status ADD VALUE IF NOT EXISTS 'deprecated'"
    )


def downgrade() -> None:
    pass
