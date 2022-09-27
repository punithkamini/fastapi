"""add foriegn-key to posts table

Revision ID: d41ae27c290d
Revises: b9eacb0c6406
Create Date: 2022-09-26 14:30:15.682012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd41ae27c290d'
down_revision = 'b9eacb0c6406'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',local_cols=['owner_id'],
                          remote_cols=['id'], ondelete="CASCADE")
    pass

def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
