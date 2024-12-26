from flask import Blueprint, redirect, url_for, render_template, request, make_response, redirect, session, current_app

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/')
def lab():
    return render_template('/lab9/lab9.html')