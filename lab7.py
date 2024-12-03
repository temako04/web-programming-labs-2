import os
from flask import Blueprint, render_template, request, jsonify, abort
import psycopg2
from psycopg2.extras import RealDictCursor

lab7 = Blueprint('lab7', __name__)

def db_connect():
    conn = psycopg2.connect(
        host='127.0.0.1',
        database='artem_konkin_knowledge_base',
        user='artem_konkin_knowledge_base',
        password='123'
    )
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab7.route('/lab7/')
def main():
    return render_template('lab7/lab7.html')

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films;")
    films = cur.fetchall()
    db_close(conn, cur)
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn, cur = db_connect()
    cur.execute("SELECT * FROM films WHERE id = %s;", (id,))
    film = cur.fetchone()
    db_close(conn, cur)
    if not film:
        abort(404, description="Фильм не найден")
    return jsonify(film)

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    title = film.get('title')
    title_ru = film.get('title_ru')
    year = film.get('year')
    description = film.get('description')

    try:
        year = int(year)
    except ValueError:
        return jsonify({'year': 'Год выпуска должен быть числом'}), 400

    errors = {}
    if not title_ru and not title:
        errors['title'] = 'Должно быть указано хотя бы одно название фильма (на русском или оригинальном)'
    if not description or len(description) > 2000:
        errors['description'] = 'Описание должно быть указано и не превышать 2000 символов'
    if not (1895 <= year <= 2024):
        errors['year'] = 'Год выпуска должен быть между 1895 и 2024'

    if errors:
        return jsonify(errors), 400

    conn, cur = db_connect()
    cur.execute(
        "INSERT INTO films (title, title_ru, year, description) VALUES (%s, %s, %s, %s) RETURNING id;",
        (title, title_ru, year, description)
    )
    film_id = cur.fetchone()['id']
    db_close(conn, cur)

    return jsonify({'id': film_id}), 201

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def update_film(id):
    """Обновить информацию о фильме"""
    film = request.get_json()
    title = film.get('title')
    title_ru = film.get('title_ru')
    year = film.get('year')
    description = film.get('description')

    try:
        year = int(year)
    except ValueError:
        return jsonify({'error': 'Год выпуска должен быть числом'}), 400

    if not title_ru or (not title and not title_ru):
        return jsonify({'error': 'Должно быть указано хотя бы одно название фильма (на русском или оригинальном)'}), 400
    if not description or len(description) > 2000:
        return jsonify({'error': 'Описание должно быть указано и не превышать 2000 символов'}), 400
    if not (1895 <= year <= 2024):
        return jsonify({'error': 'Год выпуска должен быть между 1895 и 2024'}), 400

    conn, cur = db_connect()
    cur.execute(
        "UPDATE films SET title = %s, title_ru = %s, year = %s, description = %s WHERE id = %s;",
        (title, title_ru, year, description, id)
    )
    db_close(conn, cur)

    return jsonify({'id': id}), 200

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    conn, cur = db_connect()
    cur.execute("DELETE FROM films WHERE id = %s;", (id,))
    db_close(conn, cur)
    return '', 204

