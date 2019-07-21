"""empty message

Revision ID: e5c008e1639f
Revises: 584a47abe698
Create Date: 2019-07-20 17:49:00.451830

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5c008e1639f'
down_revision = '584a47abe698'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tutors', sa.Column('is_working', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tutors', 'is_working')
    # ### end Alembic commands ###