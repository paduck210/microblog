"""delete comments table

Revision ID: 050fe8b316a3
Revises: 21f1a3ec4311
Create Date: 2020-01-08 15:23:37.086688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '050fe8b316a3'
down_revision = '21f1a3ec4311'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_comment_timestamp', table_name='comment')
    op.drop_table('comment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comment',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.VARCHAR(length=140), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('post_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_comment_timestamp', 'comment', ['timestamp'], unique=False)
    # ### end Alembic commands ###