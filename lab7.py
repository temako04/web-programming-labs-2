from flask import Blueprint, redirect, url_for, render_template, request, make_response, session, current_app, abort
import datetime

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7')
def main():
    return render_template('lab7/lab7.html')

films = [
    {
        "title": "1+1",
        "title_ru": "1+1",
        "year": 2011,
        "description": "Аристократ на коляске нанимает в сиделки\
            бывшего заключенного. Искрометная французская комедия\
            с Омаром Си"
    },
    {
        "title": "The Green Mile",
        "title_ru": "Зеленая миля",
        "year": 1999,
        "description": "Пол Эджкомб — начальник блока смертников\
            в тюрьме «Холодная гора», каждый из узников которого\
            однажды проходит «зеленую милю» по пути к месту казни.\
            Пол повидал много заключённых и надзирателей за время\
            работы. Однако гигант Джон Коффи, обвинённый в страшном\
            преступлении, стал одним из самых необычных обитателей блока."
    },
    {
        "title": "Insterstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Когда засуха, пыльные бури и вымирание растений\
            приводят человечество к продовольственному кризису, коллектив\
            исследователей и учёных отправляется сквозь червоточину\
            (которая предположительно соединяет области пространства-времени\
            через большое расстояние) в путешествие, чтобы превзойти прежние\
            ограничения для космических путешествий человека и найти планету\
            с подходящими для человечества условиями."
    },
    {
        "title": "Fight Club",
        "title_ru": "Бойцовский клуб",
        "year": 1999,
        "description": "Сотрудник страховой компании страдает хронической\
            бессонницей и отчаянно пытается вырваться из мучительно скучной\
            жизни. Однажды в очередной командировке он встречает некоего Тайлера\
            Дёрдена — харизматического торговца мылом с извращенной философией.\
            Тайлер уверен, что самосовершенствование — удел слабых, а\
            единственное, ради чего стоит жить, — саморазрушение."
    },
    {
        "title": "Forrest Gump",
        "title_ru": "Форрест Гамп",
        "year": 1994,
        "description": "Сидя на автобусной остановке, Форрест Гамп — не очень\
            умный, но добрый и открытый парень — рассказывает случайным\
            встречным историю своей необыкновенной жизни."
    },
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    
    return films[id]

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    del films[id]
    return '', 204

def validate_film(film):
    # Проверка: Русское название не может быть пустым
    if not film.get('title_ru'):
        return {'title_ru': 'Русское название не может быть пустым'}, 400

    # Проверка: Название на оригинальном языке не может быть пустым, если русское название пустое
    if not film.get('title') and not film.get('title_ru'):
        return {'title': 'Название на оригинальном языке должно быть заполнено, если русское название пустое'}, 400

    # Проверка: Год должен быть от 1895 до текущего года
    try:
        year = int(film.get('year', 0))  # Преобразуем год в целое число
    except ValueError:
        return {'year': 'Год должен быть числом'}, 400
    
    current_year = datetime.datetime.now().year
    if not (1895 <= year <= current_year):
        return {'year': f'Год должен быть между 1895 и {current_year}'}, 400

    # Проверка: Описание должно быть непустым и не более 2000 символов
    if not film.get('description'):
        return {'description': 'Описание не может быть пустым'}, 400
    if len(film['description']) > 2000:
        return {'description': 'Описание не может быть длиннее 2000 символов'}, 400
    
    return None

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        abort(404)
    film = request.get_json()

    error = validate_film(film)
    if error:
        return error

    films[id] = film
    return films[id]

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()

    error = validate_film(film)
    if error:
        return error

    films.append(film)
    return {'id': len(films) - 1}, 201
