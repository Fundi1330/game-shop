"""empty message

Revision ID: 408bd5abfa55
Revises: 8d27bb61f581
Create Date: 2023-05-25 15:19:19.928864

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '408bd5abfa55'
down_revision = '8d27bb61f581'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Game', schema=None) as batch_op:
        batch_op.add_column(sa.Column('genre', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Game', schema=None) as batch_op:
        batch_op.drop_column('genre')

    # ### end Alembic commands ###