"""Add enrollment_number and password_changed to users table

Revision ID: add_auth_fields
Revises: e20b79799835
Create Date: 2024-03-24 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_auth_fields'
down_revision = 'e20b79799835'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to users table
    op.add_column('users', sa.Column('enrollment_number', sa.String(), nullable=True))
    op.add_column('users', sa.Column('password_changed', sa.Boolean(), nullable=False, server_default='false'))
    
    # Create unique constraint on enrollment_number
    op.create_unique_constraint('uq_users_enrollment_number', 'users', ['enrollment_number'])


def downgrade() -> None:
    # Drop unique constraint
    op.drop_constraint('uq_users_enrollment_number', 'users', type_='unique')
    
    # Remove columns
    op.drop_column('users', 'password_changed')
    op.drop_column('users', 'enrollment_number')
