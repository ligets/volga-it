"""create_hospitals_rooms_tables

Revision ID: 3fed2be1ce66
Revises: 
Create Date: 2024-10-01 13:57:04.060120

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3fed2be1ce66'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('hospitals',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.Column('address', sa.String(), nullable=False),
                    sa.Column('contactPhone', sa.String(), nullable=False, unique=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('rooms',
                    sa.Column('id', sa.UUID(), nullable=False),
                    sa.Column('name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('name')
                    )
    op.create_table('hospital_mtm_room',
                    sa.Column('hospital_id', sa.UUID(), nullable=False),
                    sa.Column('rooms_id', sa.UUID(), nullable=False),
                    sa.ForeignKeyConstraint(['hospital_id'], ['hospitals.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['rooms_id'], ['rooms.id'], ondelete='CASCADE')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    op.drop_table('hospital_mtm_room')
    op.drop_table('rooms')
    op.drop_table('hospitals')
    # ### end Alembic commands ###