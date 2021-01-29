"""empty message

Revision ID: 692c29a21f98
Revises: 
Create Date: 2021-01-25 02:16:23.597767

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql  # noqa

# revision identifiers, used by Alembic.
revision = '692c29a21f98'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        'fees',
        sa.Column('expected_amount', sa.INTEGER(), nullable=True)
    )
    op.execute("UPDATE fees SET expected_amount = 35500")
    op.alter_column('fees', 'expected_amount', nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('fees', 'expected_amount')
    # ### end Alembic commands ###