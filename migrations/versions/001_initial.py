"""Initial migration

Revision ID: 001_initial
Revises: 
Create Date: 2024-03-18 14:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Create enum type for transaction status if it doesn't exist
    connection = op.get_bind()
    inspector = sa.inspect(connection)
    existing_enums = inspector.get_enums()
    
    if 'transactionstatus' not in [enum['name'] for enum in existing_enums]:
        op.execute("CREATE TYPE transactionstatus AS ENUM ('pending', 'processing', 'completed', 'failed')")
    
    # Create transactions table
    op.create_table('transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('transaction_id', sa.String(), nullable=False),
        sa.Column('sender', sa.String(), nullable=False),
        sa.Column('receiver', sa.String(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(), nullable=False),
        sa.Column('status', postgresql.ENUM('pending', 'processing', 'completed', 'failed', name='transactionstatus', create_type=False), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('error_message', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('transaction_id')
    )

def downgrade() -> None:
    op.drop_table('transactions')
    # Don't drop the enum type in downgrade as it might be used by other tables 