"""empty message

Revision ID: 4e5605a611e8
Revises: 1fcac43abb69
Create Date: 2020-03-09 15:29:14.171347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e5605a611e8'
down_revision = '1fcac43abb69'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('Category') as batch_op:
        # ### commands auto generated by Alembic - please adjust! ###
        batch_op.drop_constraint('unique_desc', type_='unique')
        # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table('Category') as batch_op:
        # ### commands auto generated by Alembic - please adjust! ###
        batch_op.create_unique_constraint('unique_desc', ['description'])
        # ### end Alembic commands ###
