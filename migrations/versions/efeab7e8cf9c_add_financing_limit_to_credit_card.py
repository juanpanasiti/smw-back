"""Add financing limit to credit card

Revision ID: efeab7e8cf9c
Revises: d91970b2deef
Create Date: 2025-01-25 01:54:35.355888

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = 'efeab7e8cf9c'
down_revision = 'd91970b2deef'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('credit_cards', sa.Column('financing_limit', sa.Numeric(precision=20, scale=2), nullable=True))
    # ### end Alembic commands ###

    # Copy the values from `limit` in the `accounts` table to `financing_limit` in `credit_cards`
    conn = op.get_bind()
    conn.execute(text("""
        UPDATE credit_cards
        SET financing_limit = accounts.limit
        FROM accounts
        WHERE accounts.id = credit_cards.account_id;
    """))



def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('credit_cards', 'financing_limit')
    # ### end Alembic commands ###
