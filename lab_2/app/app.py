from flask import Flask, render_template, url_for, request, make_response, redirect
import re


app = Flask(__name__)
application = app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/args')
def args():
    return render_template('args.html')


@app.route('/headers')
def headers():
    return render_template('headers.html')


@app.route('/cookies', methods=['GET', 'POST'])
def cookies():
    n_resp = make_response(render_template('cookies.html'))
    if request.method == 'POST':
        n_resp.set_cookie(request.form.get('key'),
                          request.form.get('value'))
    return n_resp


@app.route('/cookies/clear', methods=['GET', 'POST'])
def clear():
    n_resp = make_response(render_template('cookies.html'))
    for cookie in iter(request.cookies):
        print(cookie)
        n_resp.set_cookie(cookie, expires=0)
    return n_resp


@app.route('/tel_check', methods=['GET', 'POST'])
def tel_check():
    if request.method == 'POST':
        tel = request.form.get('tel')
        if not re.search(r'[^\d\s\(\)\-\.\+]', tel):
            d_tel = list(filter(lambda num: num.isdigit(), tel))
            if len(d_tel) == 10:
                d_tel.insert(0, '8')
            elif len(d_tel) == 11:
                d_tel[0] = '8'
            else:
                tel_error = "Недопустимый ввод. Неверное количество цифр."
                return render_template('tel_check.html', tel=tel, tel_error=tel_error)
            tel = ''.join(d_tel)
            tel = f"8-{tel[1:4]}-{tel[4:7]}-{tel[7:9]}-{tel[9:]}"
        else:
            tel_error = "Недопустимый ввод. В номере телефона встречаются недопустимые символы."
            return render_template('tel_check.html', tel=tel, tel_error=tel_error)
        return render_template('tel_check.html', tel=tel)
    return render_template('tel_check.html')