import os

SECRET_KEY = 'c2d9hhaa552gg3566sgga5562gg2683j37e5907262017d987e60de07801749'

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://std_2192_exam:12345678@std-mysql.ist.mospolytech.ru/std_2192_exam'


UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')