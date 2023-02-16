"""del test FK

Revision ID: 0004
Revises: 0003
Create Date: 2023-02-16 15:01:42.693685

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.drop_constraint('fk_charityproject_user_id_user', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('charityproject', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.INTEGER(), nullable=True))
        batch_op.create_foreign_key('fk_charityproject_user_id_user', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###