"""empty message

Revision ID: 4ed4c76c24a4
Revises: 15c502c3e24f
Create Date: 2019-07-21 20:34:36.473760

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ed4c76c24a4'
down_revision = '15c502c3e24f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('activation', sa.Boolean(), nullable=True))
    op.drop_column('students', 'is_working')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('students', sa.Column('is_working', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.drop_column('students', 'activation')
    # ### end Alembic commands ###