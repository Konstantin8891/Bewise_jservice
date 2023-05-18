"""Create questions db

Revision ID: 7e984c4111d1
Revises:
Create Date: 2023-05-16 12:33:45.902709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e984c4111d1'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'questions',
        sa.Column(
            'id', sa.Integer(), nullable=False, primary_key=True, index=True
        ),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('answer', sa.Text(), nullable=False),
        sa.Column('date_created', sa.Date(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('questions')
