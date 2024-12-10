import os
from flask import Blueprint, render_template, request, jsonify, abort, session
import psycopg2
from psycopg2.extras import RealDictCursor

rgz = Blueprint('rgz', __name__)

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

@rgz.route('/rgz/')
def main():
    return render_template('rgz/rgz.html')

# Получение всех ячеек
@rgz.route('/api/storage_cells', methods=['GET'])
def get_storage_cells():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM storage_cells ORDER BY id;")
    cells = cur.fetchall()
    db_close(conn, cur)
    return jsonify(cells)

# Бронирование ячейки
@rgz.route('/api/reserve_cell/<int:cell_id>', methods=['POST'])
def reserve_cell(cell_id):
    if 'login' not in session:
        return jsonify({'error': 'Вы должны быть авторизованы для бронирования ячейки'}), 401
    
    user_login = session['login']
    conn, cur = db_connect()

    # Получаем информацию о пользователе
    cur.execute("SELECT id FROM users WHERE login = %s;", (user_login,))
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return jsonify({'error': 'Пользователь не найден'}), 404
    
    # Проверяем, не забронирована ли ячейка
    cur.execute("SELECT * FROM storage_cells WHERE id = %s;", (cell_id,))
    cell = cur.fetchone()
    if not cell:
        db_close(conn, cur)
        return jsonify({'error': 'Ячейка не найдена'}), 404
    
    if cell['is_reserved']:
        db_close(conn, cur)
        return jsonify({'error': 'Эта ячейка уже забронирована'}), 400
    
    # Бронирование ячейки
    cur.execute("UPDATE storage_cells SET is_reserved = TRUE, reserved_by = %s WHERE id = %s;", (user['id'], cell_id))
    cur.execute("INSERT INTO reservations (user_id, cell_id) VALUES (%s, %s);", (user['id'], cell_id))
    db_close(conn, cur)

    return jsonify({'message': 'Ячейка успешно забронирована'}), 200

# Отмена бронирования
@rgz.route('/api/cancel_reservation/<int:cell_id>', methods=['POST'])
def cancel_reservation(cell_id):
    if 'login' not in session:
        return jsonify({'error': 'Вы должны быть авторизованы, чтобы отменить бронирование', 'code': 1}), 401

    user_login = session['login']
    conn, cur = db_connect()

    # Получаем информацию о пользователе
    cur.execute("SELECT id FROM users WHERE login = %s;", (user_login,))
    user = cur.fetchone()
    if not user:
        db_close(conn, cur)
        return jsonify({'error': 'Пользователь не найден', 'code': 2}), 404

    # Проверяем, забронирована ли ячейка этим пользователем
    cur.execute("""
        SELECT * FROM storage_cells WHERE id = %s AND reserved_by = %s;
    """, (cell_id, user['id']))
    cell = cur.fetchone()
    if not cell:
        db_close(conn, cur)
        return jsonify({'error': 'Вы не забронировали эту ячейку или она уже отменена', 'code': 3}), 400

    # Отмена бронирования
    try:
        cur.execute("UPDATE storage_cells SET is_reserved = FALSE, reserved_by = NULL WHERE id = %s;", (cell_id,))
        cur.execute("DELETE FROM reservations WHERE user_id = %s AND cell_id = %s;", (user['id'], cell_id))
        db_close(conn, cur)
        return jsonify({'message': 'Бронирование успешно отменено'}), 200
    except Exception as e:
        db_close(conn, cur)
        return jsonify({'error': f'Ошибка при отмене бронирования: {str(e)}', 'code': 4}), 500
