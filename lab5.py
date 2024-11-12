from flask import Blueprint, redirect, url_for, render_template, request, make_response, redirect, session
lab5 = Blueprint('lab5', __name__)


@lab5.route('/lab5/shablon')
def shablon():
    return render_template('/lab5/shablon.html')

