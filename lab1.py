from flask import Blueprint, redirect, url_for
lab1 = Blueprint('lab1', __name__)


@lab1.route("/index")
def start():
    return redirect("/menu", code=302)


@lab1.route("/lab1")
def lab():
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


@lab1.route('/lab1/oak')
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


@lab1.route('/lab1/student')
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


@lab1.route('/lab1/python')
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


@lab1.route('/lab1/camry')
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