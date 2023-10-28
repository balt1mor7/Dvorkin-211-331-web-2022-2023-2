from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app import db, app
from models import Book, Genre, User, Review, Image, Collection
from tools import BooksFilter, ImageSaver
import sqlalchemy as sa
import os
from auth import permission_check
import markdown
import bleach

bp = Blueprint('books', __name__, url_prefix='/books')

PER_PAGE = 9

BOOK_PARAMS = [
    'author', 'name', 'publishing_house', 'volume', 'created_at'
]

def params():
    return { p: request.form.get(p) for p in BOOK_PARAMS }

def search_params():
    return {
        'name': request.args.get('name'),
        'genre_ids': request.args.getlist('genre_ids'),
    }


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    books = BooksFilter(**search_params()).perform()
    reviews_count = {}
    for book in books:
        reviews_count[book.id] = len(book.reviews)
    pagination = books.paginate(page, PER_PAGE)
    books = pagination.items
    genres = Genre.query.all()
    return render_template('books/index.html',
                           books=books,
                           genres=genres,
                           pagination=pagination,
                           search_params=search_params(),
                           reviews_count = reviews_count)

@bp.route('/new')
@login_required
@permission_check('create')
def new():
    genres = Genre.query.all()
    return render_template('books/new.html',
                           genres=genres,
                            book = {})

@bp.route('/create', methods=['POST'])
@login_required
@permission_check('create')
def create():
    f = request.files.get('background_img')
    img = None
    if f and f.filename:
        img = ImageSaver(f).save()
        
    try:
        genres = request.form.getlist('genres')
        genres = list(map(Genre.query.get, genres))  
        short_desc = markdown.markdown(bleach.clean(request.form.get('short_desc')))  
        book = Book(**params())
        book.genres = genres   
        book.short_desc = short_desc

        if not img:
            db.session.rollback()
            flash('Выберите картинку', 'danger')
            genres = Genre.query.all()
            return render_template('books/new.html',
                            genres=genres, book = book)
        
        book.background_image_id = img.id

        for key in BOOK_PARAMS:
            if not getattr(book, key) or not book.short_desc or not book.genres:
                db.session.rollback()
                flash('Заполните все поля', 'danger')
                genres = Genre.query.all()
                return render_template('books/new.html',
                            genres=genres, book = book )
        
        db.session.add(book)
        db.session.commit()
        flash(f'Книга "{book.name}" была успешно добавлена!', 'success')

    except sa.exc.SQLAlchemyError:
        db.session.rollback()
        flash(f'При сохранении книги произошла ошибка', 'danger')
        genres = Genre.query.all()
        return render_template('books/new.html',
                        genres=genres, book = book)
    return redirect(url_for('books.index'))


@bp.route('/<int:book_id>/edit')
@login_required
@permission_check('update')
def edit(book_id):
    book = Book.query.get(book_id)
    genres = Genre.query.all()
    return render_template('books/update.html', 
                           book = book,
                           genres=genres)

@bp.route('/<int:book_id>/updating', methods=['POST'])
@login_required
@permission_check('update')
def update(book_id):
    parametres = params().items()
    print('='*30, '\n', parametres)
    try:
        book = Book.query.get(book_id)
        genres = request.form.getlist('genres')
        genres = list(map(Genre.query.get, genres)) 
        for key, value in parametres:
            if value:
                setattr(book, key, value)
        book.genres = genres   
        for key in BOOK_PARAMS:
            if not getattr(book, key) or not book.short_desc or not book.genres:
                db.session.rollback()
                flash('Все поля должны быть заполнены', 'danger')
                genres = Genre.query.all()
                return render_template('books/update.html',
                            genres=genres, book = book )
        db.session.commit()
        flash(f'Книга {book.name} была успешно изменена!', 'success')

    except sa.exc.SQLAlchemyError:
        flash(f'При сохранении книги произошла ошибка', 'danger')
        db.session.rollback()
        book = Book.query.get(book_id)
        genres = Genre.query.all()
        return render_template('books/update.html', 
                           book = book,
                           genres=genres)
    return redirect(url_for('books.show', book_id = book.id))

@bp.route('/<int:book_id>')
def show(book_id):
    book = Book.query.get(book_id)
    reviews_count = len(book.reviews)
    user_review = Review()
    collections = Collection.query.filter_by(user_id = current_user.id)
    if current_user.is_authenticated:
        user_review = Review.query.filter_by(user_id=current_user.id).filter_by(book_id=book_id).first()
    book_reviews = Review.query.filter_by(book_id=book_id).order_by(Review.created_at.desc()).limit(5).all()
    return render_template('books/show.html', book=book, 
                           review=user_review, book_reviews=book_reviews, reviews_count = reviews_count, collections = collections)

@bp.route('/<int:book_id>/delete', methods=['POST'])
@login_required
@permission_check('delete')
def delete(book_id):
    book = Book.query.get(book_id)
    books_image = Book.query.filter_by(background_image_id=book.bg_image.id).count()
    try:
        db.session.delete(book)
        # Неудаление обложки, если книг несколько
        if book.background_image_id:
            if books_image == 1:
                image = Image.query.get(book.background_image_id)
                if image:
                    os.remove(os.path.join(app.config['UPLOAD_FOLDER'],
                            image.storage_filename))
                db.session.delete(image)     
        db.session.commit()
        flash(f'Книга "{book.name}" успешно удалена', 'success')

    except sa.exc.SQLAlchemyError:
        flash(f'При удалении книги произошла ошибка', 'danger')
        db.session.rollback()
        return render_template('books/index.html')
    return redirect(url_for('books.index'))

@bp.route('/<int:book_id>/give_review')
@login_required
def give_review(book_id):
    book = Book.query.get(book_id)
    user = User.query.get(current_user.id)
    return render_template('books/give_review.html',
                           book=book,
                           user = user)

@bp.route('/<int:book_id>/send', methods=['POST'])
@login_required
def send_review(book_id):
    try:
        text = markdown.markdown(bleach.clean(request.form.get('text_review')))
        rating = int(request.form.get('rating_id'))
        review = Review(text=text, rating=rating, book_id=book_id, user_id=current_user.id)
        db.session.add(review)
        book = Book.query.get(book_id)
        book.rating_up(rating)
        db.session.commit()
        flash(f'Ваш отзыв был успешно отправлен!', 'success')

    except sa.exc.SQLAlchemyError:
        flash(f'При отправке отзыва произошла ошибка', 'danger')
        db.session.rollback()
        book = Book.query.get(book_id)
        user = User.query.get(current_user.id)
        return render_template('books/give_review.html',
                           book=book,
                           user = user)
    return redirect(url_for('books.show', book_id = book_id))

@bp.route('/<int:book_id>/reviews')
def reviews(book_id):
    page = request.args.get('page', 1, type=int)
    book_reviews = Review.query.filter_by(book_id=book_id)
    sort_reviews = request.args.get('sort_reviews')
    dictionary_reviews={'reviews_filter': sort_reviews, 'book_id': book_id}
    if sort_reviews == 'positive':
        book_reviews = book_reviews.order_by(Review.rating.desc())
    elif sort_reviews == 'negative':
        book_reviews = book_reviews.order_by(Review.rating.asc())
    else:
        book_reviews = book_reviews.order_by(Review.created_at.desc())
    pagination = book_reviews.paginate(page, 5)
    book_reviews = pagination.items
    return render_template('books/reviews.html', 
                            book_reviews=book_reviews, book_id=book_id,
                            pagination=pagination, params = dictionary_reviews)