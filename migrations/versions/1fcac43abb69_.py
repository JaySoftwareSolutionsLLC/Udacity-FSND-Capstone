"""empty message

Revision ID: 1fcac43abb69
Revises: 7ccd3c03c372
Create Date: 2020-03-09 13:25:40.553731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fcac43abb69'
down_revision = '7ccd3c03c372'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('Category') as batch_op:
        # ### commands auto generated by Alembic - please adjust! ###
        batch_op.alter_column('description',
                existing_type=sa.VARCHAR(length=1024),
                nullable=False)
        batch_op.alter_column('name',
                existing_type=sa.VARCHAR(length=16),
                nullable=False)
        batch_op.create_unique_constraint('unique_desc', ['description'])
        batch_op.create_unique_constraint('unique_name', ['name'])
        # ### end Alembic commands ###


def downgrade():
    with op.batch_alter_table('Category') as batch_op:
        # ### commands auto generated by Alembic - please adjust! ###
        batch_op.drop_constraint(None, 'Category', type_='unique')
        batch_op.drop_constraint(None, 'Category', type_='unique')
        batch_op.alter_column('Category', 'name',
                existing_type=sa.VARCHAR(length=16),
                nullable=True)
        batch_op.alter_column('Category', 'description',
                existing_type=sa.VARCHAR(length=1024),
                nullable=True)
        # ### end Alembic commands ###