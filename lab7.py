import os
from flask import Blueprint, redirect, url_for, render_template, request, make_response, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path
from dotenv import load_dotenv

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7')
def main():
    return render_template('lab7/lab7.html')

