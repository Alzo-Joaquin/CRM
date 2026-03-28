"""Agregar password hash a usuarios

Revision ID: 0591d21b10ce
Revises: 3d1bd52a7f49
Create Date: ...

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0591d21b10ce'
down_revision = '3d1bd52a7f49'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.add_column(sa.Column('password_hash', sa.String(length=255), nullable=True))

    op.execute(
        "UPDATE usuarios SET password_hash = 'pendiente_cambio' WHERE password_hash IS NULL"
    )

    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.alter_column('password_hash', existing_type=sa.String(length=255), nullable=False)


def downgrade():
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.drop_column('password_hash')