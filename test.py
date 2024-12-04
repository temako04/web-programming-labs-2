from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash
from os import path
from dotenv import load_dotenv

test = Blueprint('test', __name__)

load_dotenv()

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

@test.route('/test/')
def messenger_home():
    """Главная страница мессенджера."""
    if 'login' not in session:
        return redirect(url_for('lab5.login'))  # Перенаправление на страницу логина

    login = session['login']
    conn, cur = db_connect()

    # Получаем всех пользователей
    cur.execute("SELECT id, login FROM users WHERE login != %s;", (login,))
    users = cur.fetchall()

    db_close(conn, cur)
    return render_template('test/home.html', login=login, users=users)

@test.route('/test/chat/<int:receiver_id>', methods=['GET', 'POST'])
def chat(receiver_id):
    """Страница чата с конкретным пользователем."""
    if 'login' not in session:
        return redirect(url_for('lab5.login'))  # Перенаправление на страницу логина

    login = session['login']
    conn, cur = db_connect()

    # Получаем информацию о пользователе, с которым чатимся
    cur.execute("SELECT id, login FROM users WHERE id=%s;", (receiver_id,))
    receiver = cur.fetchone()

    if not receiver:
        db_close(conn, cur)
        return redirect(url_for('test.messenger_home'))  # Если пользователя нет, возвращаемся на главную страницу

    if request.method == 'POST':
        message_text = request.form.get('message')
        if message_text:
            # Сохраняем сообщение в базу данных
            cur.execute(""" 
                INSERT INTO messages (sender_id, receiver_id, message_text) 
                VALUES ((SELECT id FROM users WHERE login=%s), %s, %s); 
            """, (login, receiver_id, message_text))
            db_close(conn, cur)
            return redirect(url_for('test.chat', receiver_id=receiver_id))  # Перезагружаем страницу чата

    # Получаем все сообщения между пользователями
    cur.execute(""" 
        SELECT m.message_text, u.login, m.timestamp, m.id FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE (m.sender_id = (SELECT id FROM users WHERE login=%s) AND m.receiver_id = %s)
           OR (m.sender_id = %s AND m.receiver_id = (SELECT id FROM users WHERE login=%s))
        ORDER BY m.timestamp;
    """, (login, receiver_id, receiver_id, login))

    messages = cur.fetchall()

    # Отладочная печать структуры messages
    print(messages)  # Проверка, что передается в шаблон
    
    db_close(conn, cur)

    return render_template('test/chat.html', login=login, receiver=receiver, messages=messages)

@test.route('/test/delete_message/<int:message_id>')
def delete_message(message_id):
    """Удаление сообщения (отправленного или полученного)."""
    if 'login' not in session:
        return redirect(url_for('lab5.login'))  # Перенаправление на страницу логина

    login = session['login']
    conn, cur = db_connect()

    # Получаем ID текущего пользователя
    cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    user_id = cur.fetchone()

    if not user_id:
        db_close(conn, cur)
        return redirect(url_for('test.messenger_home'))  # Если пользователя нет, возвращаемся на главную страницу

    # Проверяем, является ли текущий пользователь отправителем или получателем сообщения
    cur.execute("""
        SELECT * FROM messages WHERE id=%s AND (sender_id = %s OR receiver_id = %s);
    """, (message_id, user_id['id'], user_id['id']))
    
    message = cur.fetchone()

    if message:
        # Удаляем сообщение
        cur.execute("DELETE FROM messages WHERE id=%s;", (message_id,))
    
    db_close(conn, cur)
    return redirect(url_for('test.messenger_home'))  # Возвращаемся на главную страницу мессенджера

@test.route('/test/admin/', methods=['GET', 'POST'])
def admin():
    """Страница для администратора (удаление пользователей)."""
    if 'login' not in session or session['login'] != 'admin':
        return redirect(url_for('lab5.login'))  # Перенаправление на страницу логина или на главную страницу

    conn, cur = db_connect()

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        if user_id:
            # Сначала удаляем все сообщения этого пользователя
            cur.execute("DELETE FROM messages WHERE sender_id=%s OR receiver_id=%s;", (user_id, user_id))
            # Затем удаляем самого пользователя
            cur.execute("DELETE FROM users WHERE id=%s;", (user_id,))
            db_close(conn, cur)
            return redirect(url_for('test.admin'))  # Обновляем страницу

    # Получаем список всех пользователей
    cur.execute("SELECT id, login FROM users;")
    users = cur.fetchall()
    db_close(conn, cur)
    return render_template('test/admin.html', users=users)
