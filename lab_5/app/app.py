
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from mysql_db import MySQL
import mysql.connector
PERMITED_PARAMS = ['login', 'password', 'last_name', 'first_name', 'middle_name', 'role_id']
EDIT_PARAMS = ['last_name', 'first_name', 'middle_name', 'role_id']

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

db = MySQL(app)

from auth import bp as auth_bp
from auth import init_login_manager, permission_check

from visits import bp as visits_bp

app.register_blueprint(auth_bp)
init_login_manager(app)

app.register_blueprint(visits_bp)

@app.before_request
def loger():
    if request.endpoint == 'static':
        return
    path = request.path
    user_id = getattr(current_user, 'id', None)
    query = 'INSERT INTO visit_logs(user_id, path) VALUES (%s, %s);'
    try:
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query, (user_id, path))
            db.connection().commit()
    except mysql.connector.errors.DatabaseError:
        db.connection().rollback()


@app.route('/')
def index():
    return render_template('index.html')

def valid_password(password):
    if len(password) < 8: 
        return 'Пароль должен содержать не менее 8 символов.'
    elif len(password) > 128: 
        return 'Пароль должен содержать не более 128 символов.'
    elif not any(char.isupper() for char in password): 
        return 'Пароль должен содержать хотя бы одну заглавную букву.'
    elif not any(char.islower() for char in password): 
        return 'Пароль должен содержать хотя бы одну строчную букву.'
    elif not any(char.isdigit() for char in password): 
        return 'Пароль должен содержать хотя бы одну цифру.'
    elif ' ' in password: 
        return 'Пароль не может содержать пробелы.'
    else: 
        return None
    

def valid_name(last_name):
    if not last_name:
        return 'Имя не может быть пустым'
    if len(last_name) > 50:
        return 'Имя должно содержать не более 50 символов'
    if ' ' in last_name: 
        return 'Имя не может содержать пробелы'
    return None

def valid_surname(first_name):
    if not first_name:
        return 'Фамилия не может быть пустой'
    if len(first_name) > 50:
        return 'Фамилия должна содержать не более 50 символов'
    if ' ' in first_name: 
        return 'Фамилия не может содержать пробелы'
    return None

def valid_login(login):
    if not login:
        return 'Логин не может быть пустым'
    # if not all(c.isalnum() or c == '_' or c == '-' for c in login):
    #     return 'Логин может содержать только латинские буквы, цифры, символы _ и -'
    if len(login) < 5:
        return 'Логин должен содержать не менее 5 символов'
    if ' ' in login: 
        return 'Логин не может содержать пробелы'
    if not all(char.isalnum() or char in '~!@#$%^&*_-+()[]{}><\/|"\'.,:;' for char in login):
        return 'Пароль не содержит недопустимые символы.'
    return None

@app.route('/users')
def users():
    query = 'SELECT users.*, roles.name AS role_name FROM users LEFT JOIN roles ON roles.id = users.role_id'
    with db.connection().cursor(named_tuple=True) as cursor:
        cursor.execute(query)
        users_list = cursor.fetchall()
    
    return render_template('users.html', users_list=users_list)

@app.route('/users/new')
@login_required
@permission_check('create')
def users_new():
    roles_list = load_roles()
    return render_template('users_new.html', roles_list=roles_list, user={})

def load_roles():
    query = 'SELECT * FROM roles;'
    cursor = db.connection().cursor(named_tuple=True)
    cursor.execute(query)
    roles = cursor.fetchall()
    cursor.close()
    return roles

def extract_params(params_list):
    params_dict = {}
    for param in params_list:
        params_dict[param] = request.form.get(param, None) or None
    return params_dict

@app.route('/users/create', methods=['POST'])
@login_required
@permission_check('create')
def create_user():
    params = extract_params(PERMITED_PARAMS)
    errors = {}

    # Валидация логина
    login_error = valid_login(params['login'])
    if login_error:
        errors['login'] = login_error

    # Валидация пароля
    password_error = valid_password(params['password'])
    if password_error:
        errors['password'] = password_error

    # Валидация имени
    name_error = valid_name(params['first_name'])
    if name_error:
        errors['first_name'] = name_error

    # Валидация фамилии
    surname_error = valid_surname(params['last_name'])
    if surname_error:
        errors['last_name'] = surname_error

    if errors:
        return render_template('users_new.html', user=params, roles_list=load_roles(), errors=errors)

    query = 'INSERT INTO users(login, password_hash, last_name, first_name, middle_name, role_id) VALUES (%(login)s, SHA2(%(password)s, 256), %(last_name)s, %(first_name)s, %(middle_name)s, %(role_id)s);'
    try:
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query, params)
            db.connection().commit()
            flash('Успешно!', 'success')
    except mysql.connector.errors.DatabaseError:
        db.connection().rollback()
        flash('При сохранении данных возникла ошибка.', 'danger')
        return render_template('users_new.html', user=params, roles_list=load_roles(), errors=errors)

    return redirect(url_for('users'))




@app.route('/users/<int:user_id>/update', methods=['POST'])
@login_required
@permission_check('edit')
def update_user(user_id):
    params = extract_params(EDIT_PARAMS)
    params['id'] = user_id

    errors = {}

    # Валидация имени
    name_error = valid_name(params['last_name'])
    if name_error:
        errors['last_name'] = name_error
        
    # Валидация фамилии
    surname_error = valid_surname(params['first_name'])
    if surname_error:
        errors['first_name'] = surname_error

    if errors:
        return render_template('users_edit.html', user=params, roles_list=load_roles(), current_user=current_user, errors=errors)    
        

    query = ('UPDATE users SET last_name=%(last_name)s, first_name=%(first_name)s, '
             'middle_name=%(middle_name)s, role_id=%(role_id)s WHERE id=%(id)s;')

    try:
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query, params)
            db.connection().commit()
            flash('Успешно!', 'success')
    except mysql.connector.errors.DatabaseError:
        db.connection().rollback()
        flash('При сохранении данных возникла ошибка.', 'danger')
        return render_template('users_edit.html', user=params, roles_list=load_roles(), current_user=current_user, errors=errors)

    return redirect(url_for('users'))



def check_password(password, password_hash):
    # Создание и инициализация объекта cursor
    cursor = db.connection().cursor(named_tuple=True)

    # SQL-запрос для сравнения хеша пароля
    query = 'SELECT IF(password_hash = SHA2(%s, 256), 1, 0) AS is_match FROM users WHERE password_hash = %s;'
    cursor.execute(query, (password, password_hash))
    result = cursor.fetchall()

    cursor.close()  # Закрытие курсора

    return len(result) > 0 and result[0].is_match == 1


@app.route('/changepassword/<int:user_id>', methods=['GET', 'POST'])
@login_required
def change_password(user_id):
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        user_id = int(request.form['user_id'])

        # Создание и инициализация объекта cursor
        cursor = db.connection().cursor(named_tuple=True)

        # Проверка корректности старого пароля
        query = 'SELECT password_hash FROM users WHERE id = %s;'
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        errors = {}  # Словарь для хранения ошибок

        if not result or not check_password(old_password, result.password_hash):
            errors['old_password'] = 'Неверный старый пароль'

        # Проверка корректности нового пароля
        validation_error = valid_password(new_password)
        if validation_error is not None:
            errors['new_password'] = validation_error

        # Проверка совпадения нового пароля и его подтверждения
        if new_password != confirm_password:
            errors['confirm_password'] = 'Подтверждение нового пароля не совпадает'

        if errors:
            cursor.close()  # Закрытие курсора
            return render_template('change_password.html', user_id=user_id, errors=errors)

        # Хеширование нового пароля на сервере при помощи SQL запроса
        query = 'UPDATE users SET password_hash = SHA2(%s, 256) WHERE id = %s;'
        cursor.execute(query, (new_password, user_id))
        try:
            db.connection().commit()
            cursor.close()
            flash('Пароль успешно изменен', 'success')
            return redirect(url_for('index'))
        except mysql.connector.errors.DatabaseError:
            db.connection().rollback()
            cursor.close()
            flash('При изменении пароля возникла ошибка.', 'danger')
            return redirect(url_for('change_password', user_id=user_id))

    return render_template('change_password.html', user_id=user_id, errors={})


@app.route('/users/<int:user_id>/edit')
@login_required
@permission_check('edit')
def edit_user(user_id):
    query = 'SELECT * FROM users WHERE users.id = %s;'
    cursor = db.connection().cursor(named_tuple=True)
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return render_template('users_edit.html', user=user, roles_list = load_roles())


@app.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@permission_check('delete')
def delete_user(user_id):
    query = 'DELETE FROM users WHERE users.id=%s;'
    try:
        cursor = db.connection().cursor(named_tuple=True)
        cursor.execute(query, (user_id,))
        db.connection().commit()
        cursor.close()
        flash('Пользователь успешно удален', 'success')
    except mysql.connector.errors.DatabaseError:
        db.connection().rollback()
        flash('При удалении пользователя возникла ошибка.', 'danger')
    return redirect(url_for('users'))


@app.route('/user/<int:user_id>')
@permission_check('show')
def show_user(user_id):

    query = '''
        SELECT users.*, roles.name AS role_name
        FROM users
        JOIN roles ON users.role_id = roles.id
        WHERE users.id = %s;
    '''
    cursor = db.connection().cursor(named_tuple=True)
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return render_template('users_show.html', user=user)