"""create users table

Revision ID: b9eacb0c6406
Revises: 089363714144
Create Date: 2022-09-24 00:11:22.202593

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b9eacb0c6406'
down_revision = '089363714144'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',sa.Column('id',sa.Integer(),nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))

    pass

def downgrade():
    op.drop_table('users')
    pass
