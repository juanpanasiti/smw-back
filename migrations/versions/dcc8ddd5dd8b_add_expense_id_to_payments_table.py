"""Add expense_id to payments table

Revision ID: dcc8ddd5dd8b
Revises: 21e511cb461a
Create Date: 2023-08-14 23:23:37.460791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dcc8ddd5dd8b'
down_revision = '21e511cb461a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payments', sa.Column('expense_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'payments', 'expenses', ['expense_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'payments', type_='foreignkey')
    op.drop_column('payments', 'expense_id')
    # ### end Alembic commands ###