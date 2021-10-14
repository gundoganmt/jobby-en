"""empty message

Revision ID: 853a7af2a25e
Revises: 43bf4fa7255a
Create Date: 2021-10-14 14:51:16.693423

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '853a7af2a25e'
down_revision = '43bf4fa7255a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Admin', sa.Column('is_admin', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Admin', 'is_admin')
    # ### end Alembic commands ###
