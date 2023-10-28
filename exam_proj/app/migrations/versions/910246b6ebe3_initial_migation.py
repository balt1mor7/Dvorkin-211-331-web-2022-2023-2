"""initial migation

Revision ID: 910246b6ebe3
Revises: 
Create Date: 2023-10-28 17:37:47.915064

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '910246b6ebe3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('genres',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_genres')),
    sa.UniqueConstraint('name', name=op.f('uq_genres_name'))
    )
    op.create_table('images',
    sa.Column('id', sa.String(length=100), nullable=False),
    sa.Column('file_name', sa.String(length=100), nullable=False),
    sa.Column('mime_type', sa.String(length=100), nullable=False),
    sa.Column('md5_hash', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_images')),
    sa.UniqueConstraint('md5_hash', name=op.f('uq_images_md5_hash'))
    )
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('desc', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_roles'))
    )
    op.create_table('books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('short_desc', sa.Text(), nullable=False),
    sa.Column('created_at', sa.String(length=4), nullable=False),
    sa.Column('publishing_house', sa.String(length=100), nullable=False),
    sa.Column('author', sa.String(length=100), nullable=False),
    sa.Column('volume', sa.Integer(), nullable=False),
    sa.Column('rating_sum', sa.Integer(), nullable=False),
    sa.Column('rating_num', sa.Integer(), nullable=False),
    sa.Column('background_image_id', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['background_image_id'], ['images.id'], name=op.f('fk_books_background_image_id_images')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_books'))
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('login', sa.String(length=100), nullable=False),
    sa.Column('password_hash', sa.String(length=200), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('first_name', sa.String(length=100), nullable=False),
    sa.Column('middle_name', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name=op.f('fk_users_role_id_roles')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('login', name=op.f('uq_users_login'))
    )
    op.create_table('book_genre',
    sa.Column('book.id', sa.Integer(), nullable=True),
    sa.Column('genre.id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book.id'], ['books.id'], name=op.f('fk_book_genre_book.id_books')),
    sa.ForeignKeyConstraint(['genre.id'], ['genres.id'], name=op.f('fk_book_genre_genre.id_genres'))
    )
    op.create_table('collections',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('desc', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_collections_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_collections')),
    sa.UniqueConstraint('name', name=op.f('uq_collections_name'))
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('text', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('book_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book_id'], ['books.id'], name=op.f('fk_reviews_book_id_books')),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('fk_reviews_user_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_reviews'))
    )
    op.create_table('book_collection',
    sa.Column('book.id', sa.Integer(), nullable=True),
    sa.Column('collection.id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['book.id'], ['books.id'], name=op.f('fk_book_collection_book.id_books')),
    sa.ForeignKeyConstraint(['collection.id'], ['collections.id'], name=op.f('fk_book_collection_collection.id_collections'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book_collection')
    op.drop_table('reviews')
    op.drop_table('collections')
    op.drop_table('book_genre')
    op.drop_table('users')
    op.drop_table('books')
    op.drop_table('roles')
    op.drop_table('images')
    op.drop_table('genres')
    # ### end Alembic commands ###
