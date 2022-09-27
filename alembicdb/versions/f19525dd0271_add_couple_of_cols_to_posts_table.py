"""add couple of cols to posts table

Revision ID: f19525dd0271
Revises: d41ae27c290d
Create Date: 2022-09-26 14:43:09.966723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f19525dd0271'
down_revision = 'd41ae27c290d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False))
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=True, server_default='TRUE'))
    pass


def downgrade():
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    pass
