from flask import Blueprint, redirect, url_for, render_template, request, make_response, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
from dotenv import load_dotenv

lab6 = Blueprint('lab6', __name__)

load_dotenv()


def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='artem_konkin_knowledge_base',
            user='artem_konkin_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()


@lab6.route('/lab6/')
def main():
    return render_template('/lab6/lab6.html')


@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']
    
    conn, cur = db_connect()

    if data['method'] == 'info':
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT number, tenant, price FROM offices;")
        else:
            cur.execute("SELECT number, tenant, price FROM offices;")
        
        offices = cur.fetchall()
        db_close(conn, cur)
        
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }
    
    login = session.get('login')
    if not login:
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'error': {'code': 1, 'message': 'Unauthorized'},
            'id': id
        }

    if data['method'] == 'booking':
        office_number = data['params']
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT tenant FROM offices WHERE number=%s;", (office_number,))
        else:
            cur.execute("SELECT tenant FROM offices WHERE number=?;", (office_number,))
        
        office = cur.fetchone()

        if office and office['tenant']:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {'code': 2, 'message': 'Already booked'},
                'id': id
            }
        
        cur.execute("UPDATE offices SET tenant=%s WHERE number=%s;", (login, office_number))
        db_close(conn, cur)
        
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    if data['method'] == 'cancellation':
        office_number = data['params']
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT tenant FROM offices WHERE number=%s;", (office_number,))
        else:
            cur.execute("SELECT tenant FROM offices WHERE number=?;", (office_number,))
        
        office = cur.fetchone()

        if not office or not office['tenant']:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {'code': 3, 'message': 'Office not rented'},
                'id': id
            }

        if office['tenant'] != login:
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {'code': 4, 'message': 'Cannot cancel another user\'s booking'},
                'id': id
            }

        cur.execute("UPDATE offices SET tenant=NULL WHERE number=%s;", (office_number,))
        db_close(conn, cur)

        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }
    
    db_close(conn, cur)
    return {
        'jsonrpc': '2.0',
        'error': {'code': -32601, 'message': 'Method not found'},
        'id': id
    }