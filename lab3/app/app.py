
from flask import Flask, render_template, session, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
application = app

app.config.from_pyfile('config.py')
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Для доступа к этой странице нужно авторизироваться.'
login_manager.login_message_category = 'warning'

class User(UserMixin):
    def __init__(self, user_id, user_login):
        self.id = user_id
        self.login = user_login

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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        remember = request.form.get('remember_me') == 'on'
        for user in get_users():
            if user['login'] == login and user['password'] == password:
                login_user(User(user['id'], user['login']), remember = remember)
                flash('Вы успешно прошли аутентификацию!', 'success')
                param_url = request.args.get('next')
                return redirect(param_url or url_for('index'))
        flash('Введён неправильный логин или пароль.', 'danger')
    return render_template('login.html')

@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/secret_page')
@login_required
def secret_page():
    return render_template('secret_page.html')

@login_manager.user_loader
def load_user(user_id):
    for user in get_users():
        if user['id'] == int(user_id):
            return User(user['id'], user['login'])
    return None

def get_users():
    users = [{
        "id": 1,
        "login": "user",
        "password": "user",
    }]
    return users