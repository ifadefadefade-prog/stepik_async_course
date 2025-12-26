from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer


revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


user_table = table(
    'products',
    column('id', Integer),
    column('title', String),
    column('price', Integer),
    column('count', Integer),
    column('description', String)
)


def upgrade():
    initial_data = [
        {'title': 'Картопля', 'price': 60,
         'count': 5, 'description': 'Картопля немытая'},
        {'title': 'Морковь', 'price': 35,
         'count': 7, 'description': 'Морковь немытая'}
    ]
    op.bulk_insert(user_table, initial_data)


def downgrade():
    op.execute("DELETE FROM products WHERE id IN (1, 2)")
