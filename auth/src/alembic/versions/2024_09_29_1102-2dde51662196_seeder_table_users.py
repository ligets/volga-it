"""seeder_table_users

Revision ID: 2dde51662196
Revises: 267f3f7c0f77
Create Date: 2024-09-29 11:51:40.106405

"""
import uuid
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session

from src.utils import get_password_hash

# revision identifiers, used by Alembic.
revision: str = '2dde51662196'
down_revision: Union[str, None] = '267f3f7c0f77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    admin_hash_password = get_password_hash('admin')
    manager_hash_password = get_password_hash('manager')
    doctor_hash_password = get_password_hash('doctor')
    user_hash_password = get_password_hash('user')

    session.execute(
        sa.text(f"""
            INSERT INTO users (id, "username", "firstName", "lastName", "hashed_password") VALUES
            ('{uuid.uuid4()}', 'admin', 'Иван', 'Иванов', '{admin_hash_password}'),
            ('{uuid.uuid4()}', 'manager', 'Василий', 'Васильев', '{manager_hash_password}'),
            ('{uuid.uuid4()}', 'doctor', 'Михаил', 'Михайлов', '{doctor_hash_password}'),
            ('{uuid.uuid4()}', 'user', 'Петр', 'Петров', '{user_hash_password}')
        """)
    )

    user_ids = session.execute(
        sa.text("""
                SELECT id, username FROM users WHERE username IN ('admin', 'manager', 'doctor', 'user')
            """)
    ).fetchall()

    # Получаем id ролей
    role_ids = session.execute(
        sa.text("""
                SELECT id, name FROM roles WHERE name IN ('Admin', 'Manager', 'Doctor', 'User')
            """)
    ).fetchall()

    user_role_mapping = {
        'admin': 'Admin',
        'manager': 'Manager',
        'doctor': 'Doctor',
        'user': 'User'
    }

    for user_id, username in user_ids:
        role_id = next(role_id for role_id, role_name in role_ids if role_name == user_role_mapping[username])
        session.execute(
            sa.text(f"""
                    INSERT INTO user_mtm_role (user_id, role_id) VALUES ('{user_id}', '{role_id}')
                """)
        )

    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)

    user_ids = session.execute(
        sa.text("""
                SELECT id FROM users WHERE username IN ('admin', 'manager', 'doctor', 'user')
            """)
    ).fetchall()

    # Удаляем записи из user_mtm_role
    for (user_id,) in user_ids:
        session.execute(
            sa.text(f"""
                    DELETE FROM user_mtm_role WHERE user_id = {user_id}
                """)
        )

    # Удаляем пользователей
    session.execute(sa.text("""
            DELETE FROM users WHERE username IN ('admin', 'manager', 'doctor', 'user')
        """))

    session.commit()
