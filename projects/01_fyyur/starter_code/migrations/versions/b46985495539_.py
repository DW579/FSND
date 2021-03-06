"""empty message

Revision ID: b46985495539
Revises: 0887e4084a03
Create Date: 2020-04-21 18:07:13.144196

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b46985495539'
down_revision = '0887e4084a03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('venue_genres',
    sa.Column('venue_genre_id', sa.Integer(), nullable=False),
    sa.Column('venue_id', sa.Integer(), nullable=True),
    sa.Column('genre_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('venue_genre_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('venue_genres')
    # ### end Alembic commands ###
