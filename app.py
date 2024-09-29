from flask import Flask, redirect, url_for, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/index")
def start():
    return redirect("/menu", code=302)
    
@app.route("/menu")
def menu():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            НГТУ, ФБ, WEB-программированиe, часть 2. Список лабораторных
        </header>

            <ol>
                <li><a href="/lab1">Первая лабораторная</a></li>
            </ol>

        <footer>
            &copy; Конкин Артём, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''

@app.route("/lab1")
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная работа 1</title>
        <link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    </head>
    <body>
        <header>
            НГТУ, ФБ, Лабораторная работа 1
        </header>

        <h1>Flask — фреймворк для создания веб-приложений на языке программирования Python, использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</h1>
        <a href="/menu">Меню</a>
        <h2>Реализованные роуты</h2>
        <ul>
            <li><a href="/lab1/oak">/lab1/oak - Дуб </a></li>
            <li><a href="/lab1/student">/lab1/student - Студент </a></li>
            <li><a href="/lab1/python">/lab1/python - Пайтон </a></li>
            <li><a href="/lab1/camry">/lab1/camry - Камри </a></li>
        </ul>

        <footer>
            &copy; Конкин Артём, ФБИ-23, 3 курс, 2024
        </footer>
    </body>
</html>
'''

@app.route('/lab1/oak')
def oak():
    return '''
<!doctype html>
<html>
<link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    <body>
        <h1>Дуб</h1>
        <img src="''' + url_for('static', filename='oak.jpg') + '''">
    </body>
</html>
'''

@app.route('/lab1/student')
def student():
    return '''
<!doctype html>
<html>
<link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    <body>
        <h1>Конкин Артём Константинович</h1>
        <img src="''' + url_for('static', filename='ngtu.jpg') + '''">
    </body>
</html>
'''

@app.route('/lab1/python')
def python():
    return '''
<!doctype html>
<html>
<link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    <body>
        <h1>Python — это высокоуровневый язык программирования, отличающийся эффективностью, простотой и универсальностью использования.</h1>
        <h1>Он широко применяется в разработке веб-приложений и прикладного программного обеспечения, а также в машинном обучении и обработке больших данных.</h1>
        <h1>За счет простого и интуитивно понятного синтаксиса является одним из распространенных языков для обучения программированию.</h1>
        <img src="''' + url_for('static', filename='python.png') + '''">
    </body>
</html>
'''

@app.route('/lab1/camry')
def camry():
    return '''
<!doctype html>
<html>
<link rel="stylesheet" type="text/css" href="''' + url_for('static', filename='lab1.css') + '''">
    <body>
        <h1>Toyota Camry — это один из самых популярных среднеразмерных седанов, производимых японским автопроизводителем Toyota.</h1>
        <h1>С момента своего запуска в 1982 году, Camry завоевала признание за надежность, долговечность и высокий уровень комфорта.</h1>
        <h1>Модель отличается элегантным дизайном и современными технологиями, что делает её привлекательным выбором как для
        городских поездок, так и для длительных путешествий.</h1>
        <img src="''' + url_for('static', filename='camry.jpg') + '''">
    </body>
</html>
'''

@app.route('/lab2/a')
def a():
    return 'ok'

@app.route('/lab2/a/')
def a1():
    return 'ok'

flower_list = ['роза', 'тюльпан', 'незабудка', 'ромашка']

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list):
        return 'Такого цветка нет', 404
    else:
        return 'Цветок: ' + flower_list[flower_id]

@app.route('/lab2/add_flower/<name>')
def add_flower(name):
    flower_list.append(name)
    return f'''
<!doctype html>
<html>
    <body>
    <h1>Добавлен новый цветок</h1>
    <p>Название нового цветка: {name} </p>
    <p>Всего цветов: {len(flower_list)}</p>
    <p>Полный список: {flower_list}</p>
    </body>
</html> 
'''

@app.route('/lab2/example')
def example():
    name = 'Конкин Артём'
    group = 'ФБИ-23'
    lab_num = '2'
    kurs = '3 курс'
    fruits = [
        {'name': 'Яблоки', 'price': 100},
        {'name': 'Груши', 'price': 120},
        {'name': 'Апельсины', 'price': 80},
        {'name': 'Мандарины', 'price': 95},
        {'name': 'Манго', 'price': 321}
    ]
    return render_template('example.html', name=name, group=group, kurs=kurs, lab_num=lab_num, fruits=fruits)