"""empty message

Revision ID: 9bf44bf2b4b2
Revises: f741d868cde5
Create Date: 2020-10-15 17:00:40.140409

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bf44bf2b4b2'
down_revision = 'f741d868cde5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('active', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'active')
    # ### end Alembic commands ###
