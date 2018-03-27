"""empty message

Revision ID: 3ce6811d877c
Revises: 04a7fa906cb8
Create Date: 2018-03-27 13:59:35.775025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3ce6811d877c'
down_revision = '04a7fa906cb8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('matchedUser', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'users', ['matchedUser'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'matchedUser')
    # ### end Alembic commands ###
