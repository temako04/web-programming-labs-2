from flask import Blueprint, redirect, url_for, render_template, request, make_response, redirect, session
lab6 = Blueprint('lab6', __name__)


@lab6.route('/lab6/')
def lab():
    return render_template('lab6/lab6.html')

