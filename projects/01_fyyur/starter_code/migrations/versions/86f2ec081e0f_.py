"""empty message

Revision ID: 86f2ec081e0f
Revises: c313b923c72c
Create Date: 2020-04-21 16:46:01.916466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86f2ec081e0f'
down_revision = 'c313b923c72c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('past_shows_count', sa.Integer(), nullable=True))
    op.add_column('artist', sa.Column('seeking_description', sa.String(length=500), nullable=True))
    op.add_column('artist', sa.Column('seeking_venue', sa.Boolean(), nullable=True))
    op.add_column('artist', sa.Column('upcoming_shows_count', sa.Integer(), nullable=True))
    op.add_column('artist', sa.Column('website', sa.String(length=120), nullable=True))
    op.drop_column('artist', 'genres')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('artist', sa.Column('genres', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_column('artist', 'website')
    op.drop_column('artist', 'upcoming_shows_count')
    op.drop_column('artist', 'seeking_venue')
    op.drop_column('artist', 'seeking_description')
    op.drop_column('artist', 'past_shows_count')
    # ### end Alembic commands ###