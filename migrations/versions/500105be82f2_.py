"""empty message

Revision ID: 500105be82f2
Revises: 1dc03b84aeb5
Create Date: 2015-07-21 20:32:13.116525

"""

# revision identifiers, used by Alembic.
revision = '500105be82f2'
down_revision = '1dc03b84aeb5'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('ends', sa.String(length=64), nullable=True))
    op.add_column('product', sa.Column('price', sa.String(length=12), nullable=True))
    op.add_column('product', sa.Column('starts', sa.String(length=64), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'starts')
    op.drop_column('product', 'price')
    op.drop_column('product', 'ends')
    ### end Alembic commands ###
