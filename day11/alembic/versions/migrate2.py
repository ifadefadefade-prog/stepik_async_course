from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer


revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


users_table = table(
    'users',
    column('id', Integer),
    column('username', String),
    column('email', String),
    column('password', String)
)


def upgrade():
    initial_data = [
        {'id': 1, 'username': 'admin', 'email':
            'admin@example.com'},
        {'id': 2, 'username': 'user', 'email':
            'user@example.com'}
    ]
    op.bulk_insert(users_table, initial_data)


def downgrade():
    op.execute('DELETE FROM users WHERE username IN ("admin", "user")')
