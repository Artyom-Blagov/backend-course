"""merge migration heads

Revision ID: 6fd4c4d9661a
Revises: d62144069e66, d98fcab4fc63
Create Date: 2026-10-03 11:11:30.978612

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "6fd4c4d9661a"
down_revision: Union[str, Sequence[str], None] = ("d62144069e66", "d98fcab4fc63")
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
