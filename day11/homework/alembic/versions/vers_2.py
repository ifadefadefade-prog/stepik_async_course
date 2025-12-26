from alembic import op
import sqlalchemy as sa


revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'products',
        sa.Column('description', sa.String, nullable=False)
    )


def downgrade():
    op.drop_column('products', 'description')
