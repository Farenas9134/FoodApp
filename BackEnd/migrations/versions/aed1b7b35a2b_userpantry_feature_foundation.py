"""UserPantry feature foundation

Revision ID: aed1b7b35a2b
Revises: 0567c5d38346
Create Date: 2026-08-17 15:31:41.516538

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import sqlite

# revision identifiers, used by Alembic.
revision = 'aed1b7b35a2b'
down_revision = '0567c5d38346'
branch_labels = None
depends_on = None


def upgrade():
    # 1. Update recipes table
    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.drop_column('ingredients')

    # 2. Recreate Relationships table cleanly with ON DELETE CASCADE
    op.drop_table('Relationships')
    op.create_table(
        'Relationships',
        sa.Column('followed_id', sa.Integer(), nullable=False),
        sa.Column('follower_id', sa.Integer(), nullable=False),
        sa.Column('followed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['followed_id'], ['user.user_id'], 
            name='fk_relationships_followed_id_user', 
            ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['follower_id'], ['user.user_id'], 
            name='fk_relationships_follower_id_user', 
            ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('followed_id', 'follower_id', name='pk_relationships')
    )


def downgrade():
    op.drop_table('Relationships')
    op.create_table(
        'Relationships',
        sa.Column('followed_id', sa.Integer(), nullable=False),
        sa.Column('follower_id', sa.Integer(), nullable=False),
        sa.Column('followed_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ['followed_id'], ['user.user_id'], 
            name='fk_relationships_followed_id_user'
        ),
        sa.ForeignKeyConstraint(
            ['follower_id'], ['user.user_id'], 
            name='fk_relationships_follower_id_user'
        ),
        sa.PrimaryKeyConstraint('followed_id', 'follower_id', name='pk_relationships')
    )

    with op.batch_alter_table('recipes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ingredients', sqlite.JSON(), nullable=False))