
from flask_login import UserMixin, LoginManager, login_user, logout_user, current_user
from flask import render_template, Blueprint, request, redirect, url_for, flash, current_app
from app import db
from users_policy import UsersPolicy
from functools import wraps

bp = Blueprint('auth', __name__, url_prefix='/auth')

def init_login_manager(app):
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message = 'Для доступа к этой странице нужно авторизироваться.'
    login_manager.login_message_category = 'warning'
    login_manager.user_loader(load_user)

class User(UserMixin):
    def __init__(self, user_id, user_login, role_id):
        self.id = user_id
        self.login = user_login
        self.role_id = role_id

    def is_admin(self):
        return self.role_id == current_app.config['ADMIN_ROLE_ID']

    def can(self, action, record = None):
        users_policy = UsersPolicy(record)
        method = getattr(users_policy, action, None)
        if method:
            return method()
        return False


def permission_check(action):
    def decor(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            user_id = kwargs.get('user_id')
            user = None
            if user_id:
                user = load_user(user_id)
            if not current_user.can(action, user):
                flash('Недостаточно прав', 'warning')
                return redirect(url_for('users'))
            return function(*args, **kwargs)
        return wrapper
    return decor


@bp.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        remember = request.form.get('remember_me') == 'on'

        query = 'SELECT * FROM users WHERE login = %s and password_hash = SHA2(%s, 256);'

        # 1' or '1' = '1' LIMIT 1#
        # user'#
        # query = f"SELECT * FROM users WHERE login = '{login}' and password_hash = SHA2('{password}', 256);"
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query, (login, password))
            # cursor.execute(query)
            print(cursor.statement)
            user = cursor.fetchone()

        if user:
            login_user(User(user.id, user.login, user.role_id), remember = remember)
            flash('Вы успешно прошли аутентификацию!', 'success')
            param_url = request.args.get('next')
            return redirect(param_url or url_for('index'))
        flash('Введён неправильный логин или пароль.', 'danger')
    return render_template('login.html')


def load_user(user_id):
    query = 'SELECT * FROM users WHERE users.id = %s;'
    cursor = db.connection().cursor(named_tuple=True)
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    if user:
        return User(user.id, user.login, user.role_id)
    return None