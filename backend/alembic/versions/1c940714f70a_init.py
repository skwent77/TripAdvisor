"""init

Revision ID: 1c940714f70a
Revises: 
Create Date: 2024-05-05 15:28:01.631139

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c940714f70a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('accommodation_info',
    sa.Column('accommodation_info_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('stars', sa.String(length=100), nullable=True),
    sa.Column('lowest_price', sa.String(length=100), nullable=True),
    sa.Column('rating', sa.String(length=100), nullable=True),
    sa.Column('location', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('accommodation_info_id')
    )
    op.create_table('plan',
    sa.Column('plan_id', sa.Integer(), nullable=False),
    sa.Column('plan_info', sa.JSON(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('plan_id')
    )
    op.create_table('plane_info',
    sa.Column('plane_info_id', sa.Integer(), nullable=False),
    sa.Column('price', sa.String(length=100), nullable=True),
    sa.Column('origin', sa.String(length=100), nullable=True),
    sa.Column('destination', sa.String(length=100), nullable=True),
    sa.Column('departure', sa.String(length=100), nullable=True),
    sa.Column('arrival', sa.String(length=100), nullable=True),
    sa.Column('airline', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('plane_info_id')
    )
    op.create_table('plan_component',
    sa.Column('component_id', sa.Integer(), nullable=False),
    sa.Column('component_type', sa.String(length=50), nullable=True),
    sa.Column('plan_id', sa.Integer(), nullable=False),
    sa.Column('plane_info_id', sa.Integer(), nullable=True),
    sa.Column('accommodation_info_id', sa.Integer(), nullable=True),
    sa.Column('activity', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['accommodation_info_id'], ['accommodation_info.accommodation_info_id'], ),
    sa.ForeignKeyConstraint(['plan_id'], ['plan.plan_id'], ),
    sa.ForeignKeyConstraint(['plane_info_id'], ['plane_info.plane_info_id'], ),
    sa.PrimaryKeyConstraint('component_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('plan_component')
    op.drop_table('plane_info')
    op.drop_table('plan')
    op.drop_table('accommodation_info')
    # ### end Alembic commands ###
