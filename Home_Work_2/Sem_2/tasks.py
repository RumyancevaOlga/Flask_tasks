# Создать страницу, на которой будет кнопка "Нажми меня", при
# нажатии на которую будет переход на другую страницу с
# приветствием пользователя по имени.

# Создать страницу, на которой будет изображение и ссылка
# на другую страницу, на которой будет отображаться форма
# для загрузки изображений.

# 📌Создать страницу, на которой будет форма для ввода логина и пароля
# 📌При нажатии на кнопку "Отправить" будет произведена проверка соответствия
# логина и пароля и переход на страницу приветствия пользователя или страницу с ошибкой.

# 📌Создать страницу, на которой будет форма для ввода текста и кнопка "Отправить"
# 📌При нажатии кнопки будет произведен подсчет количества слов в тексте и переход на страницу
# с результатом.

# 📌Создать страницу, на которой будет форма для ввода двух чисел и выбор операции
# (сложение, вычитание, умножение или деление) и кнопка "Вычислить"
# 📌При нажатии на кнопку будет произведено вычисление результата выбранной операции
# и переход на страницу с результатом.

# 📌Создать страницу, на которой будет форма для ввода имени и возраста пользователя и кнопка "Отправить"
# 📌При нажатии на кнопку будет произведена проверка возраста и переход на страницу с результатом или на
# страницу с ошибкой в случае некорректного возраста.

# 📌Создать страницу, на которой будет форма для ввода числа и кнопка "Отправить"
# 📌При нажатии на кнопку будет произведено перенаправление на страницу с результатом,
# где будет выведено введенное число и его квадрат.

# 📌Создать страницу, на которой будет форма для ввода имени и кнопка "Отправить"
# 📌При нажатии на кнопку будет произведено перенаправление на страницу с flash сообщением,
# где будет выведено "Привет, {имя}!".

# 📌Создать страницу, на которой будет форма для ввода имени и электронной почты
# 📌При отправке которой будет создан cookie файл с данными пользователя
# 📌Также будет произведено перенаправление на страницу приветствия,
# где будет отображаться имя пользователя. 📌На странице приветствия должна быть кнопка "Выйти"
# 📌При нажатии на кнопку будет удален cookie файл с данными пользователя и произведено
# перенаправление на страницу ввода имени и электронной почты.

from flask import Flask, render_template, request, abort, redirect, url_for, flash, make_response
from pathlib import Path, PurePath
from werkzeug.utils import secure_filename
from markupsafe import escape


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/hello/')
def hello1():
    return 'Привет!'


@app.route('/uploads/', methods=['GET', 'POST'])
def uploads():
    if request.method == 'POST':
        file = request.files.get('file')
        file_name = secure_filename(file.filename)
        file_name = PurePath.joinpath(Path.cwd(), 'static/images', file_name)
        file.save(file_name)
        return render_template('task2_1.html', file_name=file_name)
    return render_template('task2.html')


users = {'admin': '1234',
         'user': '0000'}


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if (username, password) in users.items():
            return 'Вы вошли'
        return f'Неправильный {escape(username)} логин или пароль'
    return render_template('task3.html')


@app.route('/count/', methods=['GET', 'POST'])
def count():
    if request.method == 'POST':
        text = request.form.get('text')
        count = len(text.split())
        return f"Количество слов: {count}"
    return render_template('task4.html')


@app.route('/calc/', methods=['GET', 'POST'])
def calc():
    if request.method == 'POST':
        num1 = int(request.form.get('number1'))
        num2 = int(request.form.get('number2'))
        operation = request.form.get('operation')
        if operation == 'add':
            return f'{num1 + num2}'
        elif operation == 'subtract':
            return f'{num1 - num2}'
        elif operation == 'multiply':
            return f'{num1 * num2}'
        elif operation == 'divide':
            return f'{num1 / num2}'
    return render_template('task5.html')


@app.route('/age', methods=['GET', 'POST'])
def age():
    if request.method == 'POST':
        username = request.form.get('username')
        age = int(request.form.get('age'))
        if age < 18:
            return abort(403)
        return f'{username}, {age} возраст прошел'
    return render_template('task6.html')


@app.errorhandler(403)
def age_not(e):
    return render_template('403.html'), 403


@app.route('/square/', methods=['GET', 'POST'])
def square():
    if request.method == 'POST':
        num = int(request.form.get('number'))
        result = num ** 2
        return redirect(url_for('square_result', num=num, result=result))
    return render_template('task7.html')


@app.route('/square_result/')
def square_result():
    num = request.args.get('num')
    result = request.args.get('result')
    return f'{num} ** 2 = {result}'


app.secret_key = b'5#y2L"F4Q8z'


@app.route('/form/', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        name = request.form.get('name')
        flash(f'Hello {name}!', 'success')
        return redirect(url_for('form'))
    return render_template('task8.html')


@app.route('/email/', methods=['GET', 'POST'])
def email():
    if request.method == 'POST':
        username = request.form.get('username')
        mail = request.form.get('email')
        response = make_response(redirect(url_for('greetings')))
        response.set_cookie('username', username)
        response.set_cookie('email', mail)
        return response
    return render_template('task9.html')


@app.route('/greetings/', methods=['GET', 'POST'])
def greetings():
    name = request.cookies.get('username')
    context = {
        'username': name
    }
    if request.method == 'POST':
        return redirect(url_for('logout'))
    return render_template('greetings.html', **context)


@app.route('/logout/')
def logout():
    resp = make_response(redirect(url_for('email')))
    resp.delete_cookie('username')
    resp.delete_cookie('email')
    return resp


if __name__ == '__main__':
    app.run(debug=True)
