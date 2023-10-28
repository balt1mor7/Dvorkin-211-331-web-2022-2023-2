from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app import db
from models import Book, Genre, User, Review, Image, Collection
from tools import BooksFilter, ImageSaver
import sqlalchemy as sa
import os
from auth import permission_check

bp = Blueprint('collections', __name__, url_prefix='/collections')

def search_params():
    return {
        'name': request.args.get('name'),
        'genre_ids': request.args.getlist('genre_ids'),
    }

@bp.route('/')
@login_required
@permission_check('show_collections')
def index():
    page = request.args.get('page', 1, type=int)
    user_id = current_user.id
    user_collections = Collection.query.filter_by(user_id=user_id)
    books_count = {}
    for collection in user_collections:
        books_count[collection.id] = len(collection.books)
    pagination = user_collections.paginate(page, 4)
    user_collections = pagination.items
    return render_template('collections/index.html',
                           collections=user_collections,
                           pagination=pagination,
                           books_count = books_count,
                           search_params = {})


@bp.route('/create', methods=['POST'])
@login_required
@permission_check('show_collections')
def create():     
    try:
        name = request.form.get('name')
        desc = request.form.get('desc')
        collection = Collection(user_id = current_user.id, name = name, desc = desc)
        db.session.add(collection)
        db.session.commit()
        flash(f'Подборка "{collection.name}" была успешно добавлена!', 'success')

    except sa.exc.SQLAlchemyError:
        flash(f'При добавлении подборки произошла ошибка', 'danger')
        db.session.rollback()
    return redirect(url_for('collections.index'))

@bp.route('/<int:book_id>/add_book', methods=['POST'])
@login_required
@permission_check('show_collections')
def add_book(book_id):
    change_collection = request.form.get('collection_id')
    try:
        collection = Collection.query.get(change_collection)
        book = Book.query.get(book_id)
        collection.books.append(book)
        db.session.commit()
        flash(f'Книга "{book.name}" была добавлена в подборку "{collection.name}"!', 'success')
    except sa.exc.SQLAlchemyError:
        flash('При добавлении книги в подборку произошла ошибка', 'danger')
        db.session.rollback()

    return redirect(url_for('books.show', book_id=book_id))

@bp.route('/<int:collection_id>')
@login_required
@permission_check('show_collections')
def show_collection(collection_id):
    collection = Collection.query.get(collection_id)
    books = collection.books

    reviews_count = {}
    for book in books:
        reviews_count[book.id] = len(book.reviews)

    genres = Genre.query.all()
    return render_template('collections/show_collection.html',
                           collection = collection, 
                           genres=genres,
                           books = books,
                            # books_count = books_count,
                        #    pagination=pagination,
                           search_params=search_params(),
                           reviews_count = reviews_count)