"""create meals table

Revision ID: 4b0eac2f8633
Revises: 
Create Date: 2022-09-11 11:46:14.109431

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b0eac2f8633'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('meals', sa.Column('meal_id', sa.Integer(),nullable=False, primary_key=True), 
    sa.Column('user_id', sa.Integer(),nullable=False),
    sa.Column('meal', sa.String(),nullable=False),
    sa.Column('quantity', sa.SmallInteger(),nullable=False),
    sa.Column('calories_consumed', sa.Float(),nullable=False),
    sa.Column('date', sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text('now()'))
    )
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
