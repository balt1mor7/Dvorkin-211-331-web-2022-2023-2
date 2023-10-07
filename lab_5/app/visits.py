
import io
from flask import render_template, Blueprint, request, send_file
from app import db
from math import ceil
from flask_login import login_required, current_user
from auth import permission_check, init_login_manager
PER_PAGE = 10

bp = Blueprint('visits', __name__, url_prefix='/visits')

def generate_report_file(records, fields):
    csv_content = '№,' + ','.join(fields) + '\n'
    for i, record in enumerate(records):
        values = [str(getattr(record, f, '')) for f in fields]
        csv_content += f'{i+1},' + ','.join(values) + '\n'
    f = io.BytesIO()
    f.write(csv_content.encode('utf-8'))
    f.seek(0)
    return f




@bp.route('/')
# Декоратор, который проверяет, авторизован ли пользователь
@login_required
def logging():

    # Получаем номер текущей страницы из GET-параметра 'page'
    page = request.args.get('page', 1, type=int)

    # Если текущий пользователь является администратором
    if current_user.is_admin():
     # Запрос для выборки всех посещений. Включает информацию о пользователе для каждой записи посещения
        query = ('SELECT visit_logs.*, users.login '
                 'FROM visit_logs LEFT JOIN users ON visit_logs.user_id = users.id '
                 'ORDER BY created_at DESC LIMIT %s OFFSET %s')
        # Выполнение запроса к БД
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query, (PER_PAGE, (page - 1) * PER_PAGE))
            logs = cursor.fetchall()

        # Запрос для подсчета количества всех записей посещений
        query = 'SELECT COUNT(*) AS count FROM visit_logs'
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query)
            count = cursor.fetchone().count
    # Если текущий пользователь не является администратором
    else:
     # Запрос для выборки всех посещений текущего пользователя. Включает информацию о пользователе для каждой записи посещения
        query = ('SELECT visit_logs.*, users.login '
                 'FROM visit_logs RIGHT JOIN users ON visit_logs.user_id = users.id '
                 'WHERE users.id = %s '
                 'ORDER BY created_at DESC LIMIT %s OFFSET %s')
        # Выполнение запроса к БД. Переменная current_user.id содержит идентификатор текущего пользователя
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query, (current_user.id, PER_PAGE, (page - 1) * PER_PAGE))
            logs = cursor.fetchall()

        # Запрос для подсчета количества всех записей посещений текущего пользователя
        query = 'SELECT COUNT(*) AS count FROM visit_logs WHERE visit_logs.user_id = %s'
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query, (current_user.id,))
            count = cursor.fetchone().count

    # Вычисляем количество страниц, необходимых для отображения всех записей посещений
    last_page = ceil(count / PER_PAGE)

    # Если был передан GET-параметр download_csv
    if request.args.get('download_csv'):
     # Запрос для выборки всех посещений. Включает информацию о пользователе для каждой записи посещения
        query = ('SELECT visit_logs.*, users.login '
                 'FROM users RIGHT JOIN visit_logs ON visit_logs.user_id = users.id '
                 'ORDER BY created_at DESC')
        # Выполнение запроса к БД
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
        # Генерируем файл CSV отчета с помощью функции generate_report_file, передавая ей параметры records, ['path', 'login', 'created_at']
        f = generate_report_file(records, ['path', 'login', 'created_at'])
        # Отправляем файл пользователю в качестве вложения
        return send_file(f, mimetype='text/csv', as_attachment=True, download_name='logs.csv')

    # Иначе отображаем шаблон logs.html, передавая ему переменные logs, last_page, current_page и PER_PAGE
    return render_template('visits/logs.html', logs=logs, last_page=last_page, current_page=page, PER_PAGE=PER_PAGE)


@bp.route('/stat/pages')
@login_required
@permission_check('change_role')
def pages_stat():
    # Получение номера текущей страницы из GET-параметра запроса, либо установка значения по умолчанию
    page = request.args.get('page', 1, type=int)
    # Формирование SQL-запроса на выборку страниц и их частоты посещений, сортировка по убыванию частоты посещений
    query = 'SELECT path, COUNT(*) as count FROM visit_logs GROUP BY path ORDER BY count DESC LIMIT %s OFFSET %s'
    with db.connection().cursor(named_tuple=True) as cursor:
        cursor.execute(query, (PER_PAGE, (page-1)*PER_PAGE))
        records = cursor.fetchall()

    # Формирование SQL-запроса для получения общего количества записей в таблице
    query = 'SELECT COUNT(*) AS count FROM (SELECT path FROM visit_logs GROUP BY path) AS paths'
    with db.connection().cursor(named_tuple=True) as cursor:
        cursor.execute(query)
        count = cursor.fetchone().count


    # Вычисление количества страниц на основе общего количества записей и количества записей на странице
    last_page = ceil(count/PER_PAGE)

    if request.args.get('download_csv'):
        query = 'SELECT path, COUNT(*) as count FROM visit_logs GROUP BY path ORDER BY count DESC'
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
        f = generate_report_file(records, ['path', 'count'])
        return send_file(f, mimetype='text/csv', as_attachment=True, download_name='pages_stat.csv')
    # Отображение шаблона pages_stat.html и передача на него объекта с данными страниц, удовлетворяющих запросу,
    # а также объектов с количеством страниц и номером текущей страницы
    return render_template('visits/pages_stat.html', records=records, last_page=last_page, current_page=page, PER_PAGE=PER_PAGE)


@bp.route('/stat/users')
@login_required
@permission_check('change_role')
def stat_user():
    page = request.args.get('page', 1, type=int)
    query = '''
        SELECT CASE WHEN user_id IS NULL THEN 'Анонимный пользователь' ELSE users.login END AS user_name, COUNT(*) AS count FROM 
        visit_logs LEFT JOIN users ON visit_logs.user_id = users.id GROUP BY user_name ORDER BY count DESC LIMIT %s OFFSET %s
        '''
    with db.connection().cursor(named_tuple=True) as cursor:
        cursor.execute(query, (PER_PAGE, (page-1)*PER_PAGE))
        records = cursor.fetchall()
    query = 'SELECT COUNT(DISTINCT user_id) as count FROM visit_logs;'
    with db.connection().cursor(named_tuple=True) as cursor:
        cursor.execute(query)
        count = cursor.fetchone().count
    last_page = ceil(count/PER_PAGE)

    if request.args.get('download_csv'):
        query = ('SELECT users.login, COUNT(visit_logs.id) AS count '
             'FROM users LEFT JOIN visit_logs ON visit_logs.user_id = users.id '
             'GROUP BY users.login '
             'ORDER BY COUNT(visit_logs.id) DESC')
        with db.connection().cursor(named_tuple=True) as cursor:
            cursor.execute(query)
            records = cursor.fetchall()
        f = generate_report_file(records, ['login', 'count'])
        return send_file(f, mimetype='text/csv', as_attachment=True, download_name='logs.csv')
    return render_template('visits/stat_user.html', records=records, last_page=last_page, current_page=page, PER_PAGE=PER_PAGE)