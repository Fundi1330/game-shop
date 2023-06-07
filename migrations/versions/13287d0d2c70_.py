"""empty message

Revision ID: 13287d0d2c70
Revises: fcbc3fbef7c7
Create Date: 2023-06-06 16:46:48.917234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13287d0d2c70'
down_revision = 'fcbc3fbef7c7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('images', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Game', schema=None) as batch_op:
        batch_op.drop_column('images')

    # ### end Alembic commands ###