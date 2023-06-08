from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к этой странице вы должны пройти аутентификацию'
login_manager.login_message_category = 'warning'

def get_users():
    users = []
    users.append({
        'id': '1',
        'login': 'user',
        'password': 'qwerty'
    })
    return users

class User(UserMixin):
    def __init__(self, id, login):
        self.id = id
        self.login = login
        
@login_manager.user_loader
def load_user(user_id):
    users = get_users()
    for user in users:
        if user_id == user['id']:
            return User(user['id'], user['login'])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/visits')
def visits():
    if 'visits_count' in session:
        session['visits_count'] += 1
    else:
        session['visits_count'] = 1
    return render_template('visits.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login = request.form['userlogin']
        password = request.form['userpassword']
        users = get_users()
        remember_check = request.form.get('remember_me') == 'on'
        for user in users:
            if login == user['login'] and password == user['password']:
                login_user(User(user['id'], user['login']), remember = remember_check)
                flash('Вы успешно прошли процедуру аутентификации!', 'success')
                next_param = request.args.get('next')
                return redirect(next_param or url_for('index'))
        flash('Вы не прошли процедуру аутентификации!', 'danger')
    return render_template('login.html')

@app.route('/secret_page')
@login_required
def secret_page():
    return render_template('secret_page.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))