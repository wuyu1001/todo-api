"""empty message

Revision ID: e27909fd77cd
Revises: 
Create Date: 2018-03-19 17:44:37.821180

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e27909fd77cd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('back_up',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('adGroupId', sa.String(length=200), nullable=True),
    sa.Column('campaignId', sa.String(length=200), nullable=True),
    sa.Column('categoryId', sa.String(length=200), nullable=True),
    sa.Column('count', sa.String(length=200), nullable=True),
    sa.Column('custId', sa.String(length=200), nullable=True),
    sa.Column('data', sa.Text(), nullable=True),
    sa.Column('itemId', sa.String(length=200), nullable=True),
    sa.Column('itemImgUrl', sa.Text(), nullable=True),
    sa.Column('itemLinkUrl', sa.String(length=200), nullable=True),
    sa.Column('itemTitle', sa.String(length=200), nullable=True),
    sa.Column('nickName', sa.String(length=200), nullable=True),
    sa.Column('operName', sa.String(length=200), nullable=True),
    sa.Column('title', sa.String(length=200), nullable=True),
    sa.Column('token', sa.String(length=200), nullable=True),
    sa.Column('ImpDate', sa.String(length=200), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('back_up')
    # ### end Alembic commands ###
