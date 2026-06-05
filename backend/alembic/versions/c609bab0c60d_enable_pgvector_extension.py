"""enable pgvector extension

Revision ID: c609bab0c60d
Revises: f157339eb0fd
Create Date: 2026-05-18 16:33:21.992891

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c609bab0c60d'
down_revision: Union[str, Sequence[str], None] = 'f157339eb0fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")


def downgrade() -> None:
    op.execute("DROP EXTENSION IF EXISTS vector")
