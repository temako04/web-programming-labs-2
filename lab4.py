from flask import Blueprint, redirect, url_for, render_template, request, make_response, redirect, session
lab4 = Blueprint('lab4', __name__)


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')

@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')

    if x2 == '0':
        return render_template('lab4/div.html', error='Нельзя делить на ноль')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum_numbers():
    x1 = request.form.get('x1') or 0
    x2 = request.form.get('x2') or 0
    result = int(x1) + int(x2)
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul_numbers():
    x1 = request.form.get('x1') or 1
    x2 = request.form.get('x2') or 1
    result = int(x1) * int(x2)
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub_numbers():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def pow_numbers():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены!')

    if x1 == '0' and x2 == '0':
        return render_template('lab4/pow.html', error='0 в степени 0 неопределено!')

    x1 = int(x1)
    x2 = int(x2)
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)

tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < 10:
        tree_count += 1

    return redirect('/lab4/tree')

users = [
    {'login': 'alex', 'password': '123', 'name': 'Lexa', 'gender': 'M'},
    {'login': 'bob', 'password': '555', 'name': 'Bobby', 'gender': 'M'},
    {'login': 'jerry', 'password': '111', 'name': 'Jerry', 'gender': 'M'},
    {'login': 'tom', 'password': '321', 'name': 'Tomik', 'gender': 'F'}
]

@lab4.route("/lab4/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            login = session['login']
            user = next((user for user in users if user['login'] == login), None)
            if user:
                return render_template("lab4/login.html", authorized=True, name=user['name'])
        return render_template("lab4/login.html", authorized=False)

    login = request.form.get('login')
    password = request.form.get('password')

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login 
            return redirect('/lab4/login')

    error = 'Неверные логин и/или пароль'
    return render_template('/lab4/login.html', error=error, authorized=False)


@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('login', None)
    return redirect('/lab4/login')

@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    message = ''
    if request.method == 'POST':
        temperature = request.form.get('temperature')

        if not temperature:
            message = 'Ошибка: не задана температура'
        else:
            try:
                temperature = float(temperature)

                if temperature < -12:
                    message = 'Не удалось установить температуру — слишком низкое значение'
                elif temperature > -1:
                    message = 'Не удалось установить температуру — слишком высокое значение'
                elif -12 <= temperature <= -9:
                    message = f'Установлена температура: {temperature}°С ❄️❄️❄️'
                elif -8 <= temperature <= -5:
                    message = f'Установлена температура: {temperature}°С ❄️❄️'
                elif -4 <= temperature <= -1:
                    message = f'Установлена температура: {temperature}°С ❄️'
            except ValueError:
                message = 'Ошибка: температура должна быть числом'

    return render_template('lab4/fridge.html', message=message)

@lab4.route('/lab4/order_grain', methods=['GET', 'POST'])
def order_grain():
    message = ''
    if request.method == 'POST':
        grain_type = request.form.get('grain_type')
        weight = request.form.get('weight')

        prices = {
            'ячмень': 12345,
            'овёс': 8522,
            'пшеница': 8722,
            'рожь': 14111
        }

        if not weight:
            message = 'Ошибка: не указан вес заказа.'
        else:
            try:
                weight = float(weight)

                if weight <= 0:
                    message = 'Ошибка: вес должен быть больше 0.'
                elif weight > 500:
                    message = 'Ошибка: такого объёма сейчас нет в наличии.'
                else:
                    if grain_type in prices:
                        total_cost = prices[grain_type] * weight
                        discount = 0

                        if weight > 50:
                            discount = total_cost * 0.10  # 10% скидка
                            total_cost -= discount
                            discount_message = f' Применена скидка за большой объём: {discount:.2f} руб.'
                        else:
                            discount_message = ''

                        message = (f'Заказ успешно сформирован. Вы заказали {grain_type}.\n'
                                   f'Вес: {weight} т. Сумма к оплате: {total_cost:.2f} руб.{discount_message}')
                    else:
                        message = 'Ошибка: выбрано несуществующее зерно.'
            except ValueError:
                message = 'Ошибка: вес должен быть числом.'

    return render_template('lab4/order_grain.html', message=message)

@lab4.route("/lab4/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("lab4/register.html", error="")

    login = request.form.get('login')
    password = request.form.get('password')
    name = request.form.get('name')
    gender = request.form.get('gender')

    if not login or not password or not name or not gender:
        error = "Все поля обязательны для заполнения."
        return render_template("lab4/register.html", error=error)

    if any(user['login'] == login for user in users):
        error = "Пользователь с таким логином уже существует."
        return render_template("lab4/register.html", error=error)

    users.append({'login': login, 'password': password, 'name': name, 'gender': gender})

    session['login'] = login
    return redirect('/lab4/login')


@lab4.route("/lab4/users", methods=['GET'])
def user_list():
    if 'login' not in session:
        return redirect('/lab4/login')

    current_login = session['login']
    return render_template("lab4/users.html", users=users, current_login=current_login)


@lab4.route("/lab4/delete_user", methods=['POST'])
def delete_user():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    login_to_delete = request.form.get('login')

    if session['login'] == login_to_delete:
        global users
        users = [user for user in users if user['login'] != login_to_delete]
        session.pop('login', None)
    return redirect('/lab4/login')


@lab4.route("/lab4/edit_user", methods=['GET', 'POST'])
def edit_user():
    if 'login' not in session:
        return redirect('/lab4/login')

    login = session['login']

    if request.method == 'POST':
        new_name = request.form.get('name')
        new_password = request.form.get('password')

        for user in users:
            if user['login'] == login:
                user['name'] = new_name if new_name else user['name']
                user['password'] = new_password if new_password else user['password']
                break

        return redirect('/lab4/users')

    user_data = next((user for user in users if user['login'] == login), None)
    return render_template("lab4/edit_user.html", user=user_data)