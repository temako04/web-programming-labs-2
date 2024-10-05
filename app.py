from flask import Flask, redirect, url_for, render_template
from lab1 import lab1
app = Flask(__name__)
app.register_blueprint(lab1)

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
            
            <ol>
                <li><a href="/lab2">Вторая лабораторная</a></li>
            </ol>

        <footer>
            &copy; Конкин Артём, ФБИ-23, 3 курс, 2024
        </footer>
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
    books = [
        {'name': '1984', 'author': 'Джордж Оруэл', 'genre': 'Дистопия', 'list':'328'},
        {'name': 'Убить пересмешника', 'author': 'Харпер Ли', 'genre': 'Роман', 'list':'281'},
        {'name': 'Мастер и Маргарита', 'author': 'Михаил Булгаков', 'genre': 'Фантастика', 'list':'448'},
        {'name': 'Гарри Поттер и философский камень', 'author': 'Дж.К. Роулинг', 'genre': 'Фэнтези', 'list':'223'},
        {'name': 'Преступление и наказание', 'author': 'Фёдор Достоевский', 'genre': 'Роман', 'list':'430'},
        {'name': 'Великий Гэтсби', 'author': 'Фрэнсис Скотт', 'genre': 'Роман', 'list':'180'},
        {'name': 'Анна Каренина', 'author': 'Лев Толстой', 'genre': 'Роман', 'list':'864'},
        {'name': 'Сияние', 'author': 'Стивен Кинг', 'genre': 'Ужасы', 'list':'447'},
        {'name': '451 градус по Фаренгейту', 'author': 'Рэй Брэдбери', 'genre': 'Научная фантастика', 'list':'158'},
        {'name': 'Маленький принц', 'author': 'Антуан де Сент-Экзюпери', 'genre': 'Роман', 'list':'96'}
    ]
    return render_template('example.html', name=name, group=group, kurs=kurs, lab_num=lab_num, fruits=fruits,books=books)

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/berries')
def berries():
    return render_template('berries.html')