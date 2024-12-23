from flask import Blueprint, redirect, url_for, render_template, request, make_response, redirect, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
from dotenv import load_dotenv
lab8 = Blueprint('lab8', __name__)

load_dotenv()

@lab8.route('/lab8/')
def lab():
    return render_template('/lab8/lab8.html')

@lab8.route('/lab8/register', methods = ['GET', 'POST'])
def register():
    return render_template('lab8/success.html',)

@lab8.route('/lab8/success')
def success():
    return render_template('/lab8/success.html')

@lab8.route('/lab8/login', methods = ['GET', 'POST'])
def login():
    return render_template('lab8/success_login.html')

@lab8.route('/lab8/success_login')
def success_login():
    return render_template('/lab8/success_login.html')

@lab8.route('/lab8/create', methods=['GET', 'POST'])
def create():
    return render_template('lab8/create_article.html')

@lab8.route('/lab8/list')
def list():
    return render_template('/lab8/articles.html')

@lab8.route('/lab8/logout')
def logout():
    return redirect('/lab8')
