from flask_app import app

from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt

from flask_app.models.user import User

bcrypt = Bcrypt()


@app.route('/')
def login_page():
    return render_template("index.html")


@app.route('/register_page')
def register_page():
    return render_template('/register_page.html')


@app.route('/register', methods=['POST'])
def register():

    if request.form['password'] != request.form['confirm_password']:
        flash("Passwords do not match!")
        return redirect('/register_page')

    if len(request.form['password']) < 1:
        flash("Password must not be blank!")
        return redirect('/register_page')

    hash = bcrypt.generate_password_hash(request.form['password'])

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hash,
    }

    if User.validate(data):
        session['uid'] = User.create(data)
        return redirect('/dashboard')
    return redirect('/register_page')


@app.route('/login', methods=['POST'])
def login():

    data = {
        'email': request.form['email']
    }

    found_user = User.find_by_email(data)

    if not found_user:
        flash("Invalid login!")
        return redirect('/')

    password_valid = bcrypt.check_password_hash(
        found_user.password, request.form['password'])

    if not password_valid:
        flash("Invalid login!")
        return redirect('/')

    session['uid'] = found_user.id
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    del session['uid']
    return redirect('/')
