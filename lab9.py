from flask import Blueprint, redirect, url_for, render_template, request, session

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/', methods=['GET', 'POST'])
def lab():
    if 'name' in session and 'age' in session and 'gender' in session and 'preference1' in session and 'preference2' in session:
        return redirect(url_for('lab9.congratulations'))
    
    if request.method == 'POST':
        session['name'] = request.form.get('name')
        return redirect(url_for('lab9.age'))
    return render_template('lab9/lab9.html')

@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    if request.method == 'POST':
        session['age'] = request.form.get('age')
        return redirect(url_for('lab9.gender'))
    return render_template('lab9/age.html')

@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    if request.method == 'POST':
        session['gender'] = request.form.get('gender')
        return redirect(url_for('lab9.preference1'))
    return render_template('lab9/gender.html')

@lab9.route('/lab9/preference1', methods=['GET', 'POST'])
def preference1():
    if request.method == 'POST':
        session['preference1'] = request.form.get('preference1')
        return redirect(url_for('lab9.preference2'))
    return render_template('lab9/preference1.html')

@lab9.route('/lab9/preference2', methods=['GET', 'POST'])
def preference2():
    if request.method == 'POST':
        session['preference2'] = request.form.get('preference2')
        return redirect(url_for('lab9.congratulations'))
    return render_template('lab9/preference2.html')

@lab9.route('/lab9/congratulations')
def congratulations():
    if 'name' not in session or 'age' not in session or 'gender' not in session or 'preference1' not in session or 'preference2' not in session:
        return redirect(url_for('lab9.lab'))
    
    name = session.get('name')
    age = session.get('age')
    gender = session.get('gender')
    preference1 = session.get('preference1')
    preference2 = session.get('preference2')

    if gender == 'male':
        greeting = f"Поздравляю тебя, {name}, желаю, чтобы ты быстро вырос, был умным..."
    else:
        greeting = f"Поздравляю тебя, {name}, желаю, чтобы ты быстро выросла, была умной..."

    if preference1 == 'tasty':
        if preference2 == 'sweet':
            image = 'candy.jpg'
            gift = "Вот тебе подарок — мешочек конфет."
        else:
            image = 'savory.jpg'
            gift = "Вот тебе подарок — сытная закуска."
    else:
        if preference2 == 'beautiful':
            image = 'flowers.jpg'
            gift = "Вот тебе подарок — букет цветов."
        else:
            image = 'art.jpg'
            gift = "Вот тебе подарок — произведение искусства."

    return render_template('lab9/congratulations.html', greeting=greeting, gift=gift, image=image)

@lab9.route('/lab9/reset')
def reset():
    session.clear()
    return redirect(url_for('lab9.lab'))