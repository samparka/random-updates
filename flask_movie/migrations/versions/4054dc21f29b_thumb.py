"""thumb

Revision ID: 4054dc21f29b
Revises: 
Create Date: 2018-04-18 18:56:21.236607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4054dc21f29b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('thumb_head_img', sa.Unicode(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'thumb_head_img')
    # ### end Alembic commands ###
