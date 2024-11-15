from flask import Blueprint, redirect, url_for, render_template, request, make_response, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
from dotenv import load_dotenv
lab5 = Blueprint('lab5', __name__)

load_dotenv()

@lab5.route('/lab5/')
def lab():
    return render_template('/lab5/lab5.html', login=session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn= psycopg2.connect(
            host = '127.0.0.1',
            database = 'artem_konkin_knowledge_base',
            user = 'artem_konkin_knowledge_base',
            password = '123'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur

def db_close(conn,cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('/lab5/register.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn,cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login,))

    if cur.fetchone():
        db_close(conn,cur)
        return render_template('lab5/register.html',
                                error="Такой пользователь уже существует")

    password_hash = generate_password_hash(password)
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("INSERT INTO users (login, password) VALUES (%s, %s;", (login, password_hash))
    else:
        cur.execute("INSERT INTO users (login, password) VALUES (?, ?);", (login, password_hash))
    

    db_close(conn,cur)
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/success')
def success():
    return render_template('/lab5/success.html')

@lab5.route('/lab5/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/login.html', error='Заполните поля')

    conn,cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login, ))
    user = cur.fetchone()

    if not user:
        db_close(conn,cur)
        return render_template('lab5/login.html',
                                error='Логин и/или пароль неверны')

    if not check_password_hash(user['password'], password):
        db_close(conn,cur)
        return render_template('lab5/login.html',
                                error='Логин и/или пароль неверны')

    session['login'] = login
    db_close(conn,cur)
    return render_template('lab5/success_login.html',login=login)

@lab5.route('/lab5/success_login')
def success_login():
    return render_template('/lab5/success_login.html')

@lab5.route('/lab5/create', methods=['GET', 'POST'])
def create():
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    if request.method == 'GET':
        return render_template('lab5/create_article.html')

    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = 'is_favorite' in request.form 
    is_public = 'is_public' in request.form 

    if not title or not article_text:
        return render_template('lab5/create_article.html', error="Название и текст статьи обязательны.")

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    login_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("""
            INSERT INTO articles (login_id, title, article_text, is_favorite, is_public) 
            VALUES (%s, %s, %s, %s, %s);
        """, (login_id, title, article_text, is_favorite, is_public))
    else:
        cur.execute("""
            INSERT INTO articles (login_id, title, article_text, is_favorite, is_public) 
            VALUES (?, ?, ?, ?, ?);
        """, (login_id, title, article_text, is_favorite, is_public))

    db_close(conn, cur)
    return redirect('/lab5')

@lab5.route('/lab5/list')
def list():
    login = session.get('login')

    conn, cur = db_connect()

    if login:
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT * FROM articles 
                WHERE is_public=TRUE OR login_id = (SELECT id FROM users WHERE login=%s)
                ORDER BY is_favorite DESC;
            """, (login,))
        else:
            cur.execute("""
                SELECT * FROM articles 
                WHERE is_public=TRUE OR login_id = (SELECT id FROM users WHERE login=?)
                ORDER BY is_favorite DESC;
            """, (login,))
    else:

        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("""
                SELECT * FROM articles WHERE is_public=TRUE
                ORDER BY is_favorite DESC;
            """)
        else:
            cur.execute("""
                SELECT * FROM articles WHERE is_public=TRUE
                ORDER BY is_favorite DESC;
            """)

    articles = cur.fetchall()

    db_close(conn, cur)

    return render_template('/lab5/articles.html', articles=articles)

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')
    
@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("SELECT * FROM articles WHERE id=?;", (article_id,))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return redirect('/lab5/list')

    if request.method == 'GET':
        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title')
    article_text = request.form.get('article_text')

    if not title or not article_text:
        return render_template('lab5/edit_article.html', article=article, error="Заполните все поля")

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("UPDATE articles SET title=%s, article_text=%s WHERE id=%s;", (title, article_text, article_id))
    else:
        cur.execute("UPDATE articles SET title=?, article_text=? WHERE id=?;", (title, article_text, article_id))

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/delete/<int:article_id>')
def delete(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("DELETE FROM articles WHERE id=%s;", (article_id,))
    else:
        cur.execute("DELETE FROM articles WHERE id=?;", (article_id,))

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/users')
def users():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users;")
    else:
        cur.execute("SELECT login FROM users;")
    
    users = cur.fetchall()

    db_close(conn, cur)

    return render_template('lab5/users.html', users=users)
