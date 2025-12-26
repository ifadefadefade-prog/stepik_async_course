from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer, Enum
from models import ProductStatus

revision = '006'
down_revision = '005'
branch_labels = None
depends_on = None


user_table = table(
    'products',
    column('id', Integer),
    column('title', String),
    column('price', Integer),
    column('count', Integer),
    column('description', String),
    column('status', Enum(ProductStatus, name="product_status"))
)


def upgrade():
    initial_data = [
        {'title': 'Пизда', 'price': 60,
         'count': 5, 'description': 'С ушами'}
    ]
    op.bulk_insert(user_table, initial_data)


def downgrade():
    op.execute("DELETE FROM products WHERE title='Пизда'")
