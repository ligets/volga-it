"""seeder_table_roles

Revision ID: 267f3f7c0f77
Revises: 6da2b2e0fd4d
Create Date: 2024-09-29 11:43:29.795045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

# revision identifiers, used by Alembic.
revision: str = '267f3f7c0f77'
down_revision: Union[str, None] = '6da2b2e0fd4d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    session.execute(sa.text("""
        INSERT INTO roles (name) VALUES
            ('Admin'),
            ('Manager'),
            ('Doctor'),
            ('User')
    """))

    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    session.execute(sa.text("""
        DELETE FROM roles WHERE name IN ('Admin', 'Manager', 'Doctor', 'User')
    """))

    session.commit()

