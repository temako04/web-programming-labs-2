from flask import Blueprint, redirect, url_for, render_template, request, make_response
lab3 = Blueprint('lab3', __name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')

    if name is None:
        name = "Аноним"
    if age is None:
        age = "сколько-то"
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'green')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')

    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10   
    
    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    backgroundcolor = request.args.get('background-color')
    fontsize = request.args.get('fontsize')
    fontweight = request.args.get('fontweight')

    resp = make_response(redirect('/lab3/settings'))

    if color:
        resp.set_cookie('color', color)
    
    if backgroundcolor:
        resp.set_cookie('background-color', backgroundcolor)
    
    if fontsize:
        resp.set_cookie('fontsize', fontsize)

    if fontweight:
        resp.set_cookie('fontweight', fontweight)

    if not (color or backgroundcolor or fontsize or fontweight):
        color = request.cookies.get('color')
        backgroundcolor = request.cookies.get('background-color')
        fontsize = request.cookies.get('fontsize')
        fontweight = request.cookies.get('fontweight')
        resp = make_response(render_template('lab3/settings.html', color=color, backgroundcolor=backgroundcolor, fontsize=fontsize, fontweight=fontweight))
    return resp


@lab3.route('/lab3/form2/')
def form2():
    errors = {}
    pass_name = request.args.get('pass_name')
    if pass_name == '':
        errors['pass_name'] = 'Заполните поле!'

    shelf = request.args.get('shelf')
    bedding = request.args.get('bedding') == 'on'
    luggage = request.args.get('luggage') == 'on'
    
    age = request.args.get('age')
    if age == None:
        errors['age'] = ''
    elif age =='':
        errors['age'] = 'Заполните поле!'
    else:
        age = int(age)
        if age < 1 or age > 120:
            errors['age'] = 'Возраст должен быть от 1 до 120 лет!'

    departure = request.args.get('departure')
    if departure == '':
        errors['departure'] = 'Заполните поле!'

    destination = request.args.get('destination')
    if destination == '':
        errors['destination'] = 'Заполните поле!'

    date = request.args.get('date')
    if date == '':
        errors['date'] = 'Заполните поле!'
    
    insurance = request.args.get('insurance') == 'on'

    if 'age' in errors:
        price = 0
        ticket_type = ''
    else:
        if age >= 18:
            base_price = 1000
            ticket_type = 'Взрослый'
        else:
            base_price = 700
            ticket_type = 'Детский'

        if shelf in ['lower', 'lower_side']:
            base_price += 100
        if bedding:
            base_price += 75
        if luggage:
            base_price += 250
        if insurance:
            base_price += 150

        price = base_price

    return render_template('lab3/form2.html', errors=errors, pass_name=pass_name, shelf=shelf,
                           bedding=bedding, luggage=luggage, age=age, departure=departure,
                           destination=destination, date=date, insurance=insurance,
                           ticket_type=ticket_type, price=price)


@lab3.route('/lab3/del_cookie_2')
def del_cookie_2():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('background-color')
    resp.delete_cookie('fontsize')
    resp.delete_cookie('fontweight')
    return resp

products = [
    {'name': 'Samsung Galaxy S23', 'price': 74990, 'brand': 'Samsung', 'color': 'черный'},
    {'name': 'Apple iPhone 14', 'price': 79990, 'brand': 'Apple', 'color': 'белый'},
    {'name': 'Xiaomi 13', 'price': 59990, 'brand': 'Xiaomi', 'color': 'синий'},
    {'name': 'OnePlus 11', 'price': 59990, 'brand': 'OnePlus', 'color': 'серый'},
    {'name': 'Google Pixel 7', 'price': 64990, 'brand': 'Google', 'color': 'красный'},
    {'name': 'Sony Xperia 1 IV', 'price': 89990, 'brand': 'Sony', 'color': 'зеленый'},
    {'name': 'Huawei P50 Pro', 'price': 59990, 'brand': 'Huawei', 'color': 'черный'},
    {'name': 'Oppo Find X5', 'price': 64990, 'brand': 'Oppo', 'color': 'белый'},
    {'name': 'Vivo X80', 'price': 54990, 'brand': 'Vivo', 'color': 'синий'},
    {'name': 'Realme GT 2 Pro', 'price': 49990, 'brand': 'Realme', 'color': 'серый'},
    {'name': 'Asus ROG Phone 6', 'price': 79990, 'brand': 'Asus', 'color': 'красный'},
    {'name': 'Motorola Edge 30', 'price': 32990, 'brand': 'Motorola', 'color': 'зеленый'},
    {'name': 'Nokia X30', 'price': 27990, 'brand': 'Nokia', 'color': 'черный'},
    {'name': 'Honor 70', 'price': 34990, 'brand': 'Honor', 'color': 'белый'},
    {'name': 'ZTE Axon 20', 'price': 29990, 'brand': 'ZTE', 'color': 'синий'},
    {'name': 'LG Velvet', 'price': 34990, 'brand': 'LG', 'color': 'серый'},
    {'name': 'Tecno Camon 19', 'price': 19990, 'brand': 'Tecno', 'color': 'красный'},
    {'name': 'Infinix Zero 5G', 'price': 24990, 'brand': 'Infinix', 'color': 'зеленый'},
    {'name': 'Samsung Galaxy A54', 'price': 34990, 'brand': 'Samsung', 'color': 'черный'},
    {'name': 'Apple iPhone SE (3rd Gen)', 'price': 39990, 'brand': 'Apple', 'color': 'белый'},
]

@lab3.route('/lab3/products')
def index():
    return render_template('lab3/products.html')

@lab3.route('/lab3/results')
def search():
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    
    filtered_products = [
        product for product in products
        if int(min_price) <= product['price'] <= int(max_price)
    ]
    
    return render_template('lab3/results.html', products=filtered_products)