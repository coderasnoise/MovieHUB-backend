"""added thumbnail

Revision ID: 7c28dd2578a5
Revises: 43c92d0d7345
Create Date: 2024-05-15 15:19:08.970272

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '7c28dd2578a5'
down_revision: Union[str, None] = '43c92d0d7345'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('movies', sa.Column('thumbnail', sa.String(length=255), nullable=True))
    op.drop_column('movies', 'thumbnail_url')
    op.add_column('series', sa.Column('thumbnail', sa.String(length=255), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('series', 'thumbnail')
    op.add_column('movies', sa.Column('thumbnail_url', mysql.VARCHAR(length=255), nullable=True))
    op.drop_column('movies', 'thumbnail')
    # ### end Alembic commands ###