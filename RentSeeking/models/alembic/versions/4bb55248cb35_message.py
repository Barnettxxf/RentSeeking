"""message

Revision ID: 4bb55248cb35
Revises: 
Create Date: 2018-06-20 17:22:52.798843

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '4bb55248cb35'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('record')
    op.drop_table('detailinfo')
    op.drop_table('baseinfo')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('baseinfo',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('apm_name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('apm_url', mysql.TEXT(), nullable=False),
    sa.Column('cell_name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('cell_type', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('area', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('built_year', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('price', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('subway', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('spider', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('created_at', mysql.DATETIME(), nullable=False),
    sa.Column('updated_at', mysql.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('detailinfo',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('apm_name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('price', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('area', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('floor', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('apm_detail_url', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('traffication', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('location', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('cell_type', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('orientation', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('contact', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('contact_identity', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('phone', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('spider', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('created_at', mysql.DATETIME(), nullable=False),
    sa.Column('updated_at', mysql.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    op.create_table('record',
    sa.Column('id', mysql.INTEGER(display_width=11), nullable=False),
    sa.Column('base_info_count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('detail_info_count', mysql.INTEGER(display_width=11), autoincrement=False, nullable=False),
    sa.Column('spider', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('cost_time', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('created_at', mysql.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8',
    mysql_engine='InnoDB'
    )
    # ### end Alembic commands ###
