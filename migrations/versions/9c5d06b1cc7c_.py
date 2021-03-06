"""empty message

Revision ID: 9c5d06b1cc7c
Revises: 
Create Date: 2018-03-26 23:31:47.287481

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c5d06b1cc7c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('locations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('gid', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=127), nullable=True),
    sa.Column('address', sa.String(length=127), nullable=True),
    sa.Column('phoneNumber', sa.String(length=50), nullable=True),
    sa.Column('priceLevel', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('currentUserCount', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('gid')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=254), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('name', sa.String(length=32), nullable=True),
    sa.Column('surname', sa.String(length=32), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('lastCheckIn', sa.DateTime(), nullable=True),
    sa.Column('checkInLocation', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['checkInLocation'], ['locations.gid'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('locations')
    # ### end Alembic commands ###
