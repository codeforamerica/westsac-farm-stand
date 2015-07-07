"""empty message

Revision ID: 15e97d88efd8
Revises: fc814e4e8c5
Create Date: 2015-07-06 19:53:47.741259

"""

# revision identifiers, used by Alembic.
revision = '15e97d88efd8'
down_revision = 'fc814e4e8c5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('available', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product')
    ### end Alembic commands ###
