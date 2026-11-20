"""initial database schema

Revision ID: f3b13c95abe2
Revises: None
Create Date: 2026-11-16 08:19:52.918358

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f3b13c95abe2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
        sa.Column('id',sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('username', sa.VARCHAR(length = 100), nullable = False),
        sa.Column('email',sa.VARCHAR(length=150),nullable=False),
        sa.Column('hashed_password',sa.VARCHAR(length=255),nullable=False),
        sa.Column('is_active',sa.Boolean(),nullable=False),
        sa.PrimaryKeyConstraint('id',name=op.f('users_pkey')),
        sa.UniqueConstraint('username',name=op.f('users_username_key')),
        sa.UniqueConstraint('email',name=op.f('users_email_key'))
    )

    op.create_table('restaurants',
        sa.Column('id',sa.INTEGER(),autoincrement=True,nullable=False),
        sa.Column('name',sa.VARCHAR(length=100),nullable=False),
        sa.Column('location',sa.VARCHAR(length=100),nullable=False),
        sa.Column('owner_id',sa.INTEGER(),nullable=False),
        sa.ForeignKeyConstraint(['owner_id'],['users.id'],name=op.f('restaurants_owner_id_fkey')),
        sa.PrimaryKeyConstraint('id',name=op.f('restaurants_pkey'))
    )
    op.create_table('foods',
        sa.Column('id',sa.INTEGER(),autoincrement=True,nullable=False),
        sa.Column('name',sa.VARCHAR(length=100),nullable=False),
        sa.Column('description',sa.VARCHAR(length=500),nullable=False),
        sa.Column('price',sa.Float(),nullable=False),
        sa.Column('restaurant_id',sa.INTEGER(),nullable=False),
        sa.ForeignKeyConstraint(['restaurant_id'],['restaurants.id'],name=op.f('foods_restaurant_id_fkey')),
        sa.PrimaryKeyConstraint('id',name=op.f('foods_pkey'))
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("foods")
    op.drop_table("restaurants")
    op.drop_table("users")