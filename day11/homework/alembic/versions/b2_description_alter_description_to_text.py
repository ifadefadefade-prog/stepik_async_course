from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2_description'
down_revision: Union[str, Sequence[str], None] = '006'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('products',
                    'description', existing_type=sa.String(length=255),
                    type_=sa.Text(),
                    nullable=False)


def downgrade() -> None:
    op.alter_column('products',
                    'description', existing_type=sa.String(length=255),
                    type_=sa.Text(),
                    nullable=True)
