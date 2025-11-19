"""add_refresh_tokens_table

Revision ID: a3035d06cc1e
Revises: c0ac1cd24537
Create Date: 2025-11-16 22:59:02.165014

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = 'a3035d06cc1e'
down_revision = 'c0ac1cd24537'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create refresh_tokens table
    op.create_table(
        'refresh_tokens',
        sa.Column('id', UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('token_hash', sa.String(64), nullable=False, unique=True),
        sa.Column('expires_at', sa.DateTime(), nullable=False),
        sa.Column('revoked', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('revoked_at', sa.DateTime(), nullable=True),
        sa.Column('device_info', sa.String(255), nullable=True),
        sa.Column('ip_address', sa.String(45), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    
    # Create indexes
    op.create_index('idx_refresh_tokens_token_hash', 'refresh_tokens', ['token_hash'])
    op.create_index('idx_refresh_tokens_expires_at', 'refresh_tokens', ['expires_at'])
    op.create_index('idx_refresh_tokens_revoked', 'refresh_tokens', ['revoked'])
    op.create_index('idx_user_valid_tokens', 'refresh_tokens', ['user_id', 'revoked', 'expires_at'])


def downgrade() -> None:
    # Drop indexes
    op.drop_index('idx_user_valid_tokens', table_name='refresh_tokens')
    op.drop_index('idx_refresh_tokens_revoked', table_name='refresh_tokens')
    op.drop_index('idx_refresh_tokens_expires_at', table_name='refresh_tokens')
    op.drop_index('idx_refresh_tokens_token_hash', table_name='refresh_tokens')
    
    # Drop table
    op.drop_table('refresh_tokens')

