"""create posts table

Revision ID: 089363714144
Revises: 
Create Date: 2022-09-23 23:31:00.431539

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '089363714144'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), primary_key=True, nullable=False), sa.Column('title', sa.String(), nullable=False), sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
