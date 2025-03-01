"""Add job_posting_stats_view

Revision ID: 022fdd04d856
Revises: 8fcad645974f
Create Date: 2025-03-01 14:50:43.791427

"""
import os

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '022fdd04d856'
down_revision = '8fcad645974f'
branch_labels = None
depends_on = None


def upgrade():
    migration_dir = os.path.dirname(__file__)
    base_dir = os.path.dirname(migration_dir)
    sql_file_path = os.path.join(base_dir, 'views', 'job_posting_stats_view.sql')

    with open(sql_file_path, 'r') as file:
        view_sql = file.read()
    op.execute(view_sql)


def downgrade():
    op.execute("DROP VIEW IF EXISTS public.job_posting_stats_view;")