from flask import Flask, render_template, request
from flask import make_response

app = Flask(__name__)
application=app

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/headers')
def headers():
    return render_template('headers.html')

@app.route('/args')
def args():
    return render_template('args.html')

@app.route('/cookies')
def cookies():
    resp = make_response(render_template('cookies.html'))
    if "name" in request.cookies:
        resp.delete_cookie("name")
    else:
        resp.set_cookie("name", "value")
    return resp

@app.route('/form', methods=['GET', 'POST'])
def form():
    return render_template('form.html')

@app.route("/formcheck", methods=['GET', 'POST'])
def form_check():
    if request.method == 'POST':
        context = {}
        num = []
        others = []
        allowed = [' ', '(', ')', '-', '.', '+']
        for i in request.form['number']:
            if i.isdigit():
                num.append(i)
            else:
                others.append(i)
        if len(num) < 10 and (num[0] != '7' or num[0] != '8'):
            context = 'номер слишком короткий'
        elif len(others) == 3 and (len(num) == 10):
            if (others[0]=='.') and (others[1]=='.') and (others[2]=='.'):
                number = '8-' + str(num[0]) + str(num[1]) + str(num[2]) + '-' + str(num[3]) + str(num[4]) + str(num[5]) +'-' + str(num[6]) + str(num[7]) + '-' + str(num[8]) + str(num[9])
                print('верный формат')
            else:
                context = 'номер содержит недопустимые символы'
        elif (int(num[0]) == 8 or (int(num[0])==7 and others[0]=='+')) and len(num) == 11:
            number = '8-' + str(num[1]) + str(num[2]) + str(num[3]) + '-' + str(num[4]) + str(num[5]) + str(num[6]) +'-' + str(num[7]) + str(num[8]) + '-' + str(num[9]) + str(num[10])
            print('верный формат')
        else:
            context = 'номер слишком длинный'
        for symbol in others:
            if symbol not in allowed:
                context = 'номер содержит недопустимые символы'
        if context:
            return render_template('form_check.html', context=context )
        else:
            return render_template('form_check.html', number=number)
    return render_template('form_check.html')


@app.route('/calc', methods=['GET', 'POST'])
def calc():
    answer=''
    error_text=''
    if request.method=='POST':
        try:
            first_num = int(request.form['firstnumber'])
            second_num = int(request.form['secondnumber'])
        except ValueError:
            error_text='Был передан текст. Введите, пожалуйста, число.'
            return render_template('calc.html', answer=answer, error_text=error_text)
        operation = request.form['operation']
        if operation == '+':
            answer = first_num + second_num
        elif operation == '-':
            answer = first_num - second_num
        elif operation == '*':
            answer = first_num * second_num
        elif operation == '/':
            try:
                answer = first_num / second_num
            except ZeroDivisionError:
                error_text = 'На ноль делить нельзя'
    return render_template('calc.html', answer=answer, error_text=error_text)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404