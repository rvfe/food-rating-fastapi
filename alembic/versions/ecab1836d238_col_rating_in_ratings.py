"""col rating in ratings

Revision ID: ecab1836d238
Revises: 4031342b0a40
Create Date: 2023-02-06 17:43:02.154970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecab1836d238'
down_revision = '4031342b0a40'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ratings', sa.Column('rating', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('ratings', 'rating')
    # ### end Alembic commands ###