"""add_bill_group_and_bill_support

Revision ID: b4c2e8f91d3a
Revises: a3035d06cc1e
Create Date: 2025-12-30 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'b4c2e8f91d3a'
down_revision = 'a3035d06cc1e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create bill_groups table (inherits from accounts via polymorphism)
    op.create_table(
        'bill_groups',
        sa.Column('account_id', UUID(as_uuid=True), sa.ForeignKey('accounts.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    )

    # Add bill-specific columns to expenses table
    op.add_column('expenses', sa.Column('frequency', sa.String(20), nullable=True))
    op.add_column('expenses', sa.Column('next_bill_month', sa.Integer(), nullable=True))
    op.add_column('expenses', sa.Column('next_bill_year', sa.Integer(), nullable=True))
    op.add_column('expenses', sa.Column('notes', sa.Text(), server_default='', nullable=False))

    # Create indexes for bill-specific queries
    op.create_index('idx_expenses_frequency', 'expenses', ['frequency'])
    op.create_index('idx_expenses_next_bill', 'expenses', ['next_bill_year', 'next_bill_month'])
    op.create_index('idx_expenses_expense_type', 'expenses', ['expense_type'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_expenses_expense_type', table_name='expenses')
    op.drop_index('idx_expenses_next_bill', table_name='expenses')
    op.drop_index('idx_expenses_frequency', table_name='expenses')

    # Drop bill-specific columns from expenses table
    op.drop_column('expenses', 'notes')
    op.drop_column('expenses', 'next_bill_year')
    op.drop_column('expenses', 'next_bill_month')
    op.drop_column('expenses', 'frequency')

    # Drop bill_groups table
    op.drop_table('bill_groups')
