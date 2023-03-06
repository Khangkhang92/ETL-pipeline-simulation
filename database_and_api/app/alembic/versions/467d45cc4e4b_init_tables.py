"""Init tables

Revision ID: 467d45cc4e4b
Revises: 
Create Date: 2023-03-02 08:52:10.343748

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "467d45cc4e4b"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "index_name",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("index_id", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("index_id"),
    )
    op.create_table(
        "index_frame_h1",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("indexId", sa.String(), nullable=True),
        sa.Column("chartOpen", sa.Float(), nullable=True),
        sa.Column("chartLow", sa.Float(), nullable=True),
        sa.Column("chartHigh", sa.Float(), nullable=True),
        sa.Column("chartClose", sa.Float(), nullable=True),
        sa.Column("totalQtty", sa.BigInteger(), nullable=True),
        sa.Column("totalValue", sa.BigInteger(), nullable=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("time", sa.Time(), nullable=True),
        sa.Column("dateTime", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["indexId"],
            ["index_name.index_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("indexId", "dateTime", name="h1_upsert_key_un"),
    )
    op.create_table(
        "index_frame_m1",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("indexId", sa.String(), nullable=True),
        sa.Column("chartOpen", sa.Float(), nullable=True),
        sa.Column("chartLow", sa.Float(), nullable=True),
        sa.Column("chartHigh", sa.Float(), nullable=True),
        sa.Column("chartClose", sa.Float(), nullable=True),
        sa.Column("totalQtty", sa.BigInteger(), nullable=True),
        sa.Column("totalValue", sa.BigInteger(), nullable=True),
        sa.Column("valueMA30", sa.BigInteger(), nullable=True),
        sa.Column("valueMA14", sa.BigInteger(), nullable=True),
        sa.Column("valueMA7", sa.BigInteger(), nullable=True),
        sa.Column("date", sa.Date(), nullable=True),
        sa.Column("time", sa.Time(), nullable=True),
        sa.Column("dateTime", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["indexId"],
            ["index_name.index_id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("indexId", "dateTime", name="m1_upsert_key_un"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("index_frame_m1")
    op.drop_table("index_frame_h1")
    op.drop_table("index_name")
    # ### end Alembic commands ###
