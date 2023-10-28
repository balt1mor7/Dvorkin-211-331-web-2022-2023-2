import hashlib
import uuid
import os
from werkzeug.utils import secure_filename
from models import Book, Image
from app import db, app

class BooksFilter:
    def __init__(self, name, genre_ids):
        self.name = name
        self.genre_ids = genre_ids
        self.query = Book.query

    def perform(self):
        self.__filter_by_name()
        self.__filter_by_genre_ids()
        return self.query.order_by(Book.created_at.desc())

    def __filter_by_name(self):
        if self.name:
            self.query = self.query.filter(
                Book.name.ilike('%' + self.name + '%'))

    def __filter_by_genre_ids(self):
        if self.genre_ids:
            self.query = self.query.filter(
                Book.genre_id.in_(self.genre_ids))

class ImageSaver:
    def __init__(self, file):
        self.file = file

    def save(self):
        self.img = self.__find_by_md5_hash()
        if self.img is not None:
            return self.img
        file_name = secure_filename(self.file.filename)
        self.img = Image(
            id=str(uuid.uuid4()),
            file_name=file_name,
            mime_type=self.file.mimetype,
            md5_hash=self.md5_hash)
        self.file.save(
            os.path.join(app.config['UPLOAD_FOLDER'],
                         self.img.storage_filename))
        db.session.add(self.img)
        db.session.commit()
        return self.img

    def __find_by_md5_hash(self):
        self.md5_hash = hashlib.md5(self.file.read()).hexdigest()
        self.file.seek(0)
        return Image.query.filter(Image.md5_hash == self.md5_hash).first()