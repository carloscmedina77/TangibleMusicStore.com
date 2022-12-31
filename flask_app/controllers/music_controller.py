from flask_app import app

from flask import render_template, redirect, session, request

from flask_app.models.user import User
from flask_app.models.music import Music


@app.route('/dashboard')
def dashboard():

    if not 'uid' in session:
        return redirect('/')

    data = {
        'id': session['uid']
    }
    logged_in_user = User.find_by_id(data)

    musics = Music.get_all_musics()

    return render_template("dashboard.html", user=logged_in_user, musics=musics)


@app.route('/new_music')
def new_music():

    if not 'uid' in session:
        return redirect('/')

    return render_template("new_music.html")


@app.route('/create_music', methods=['POST'])
def create_music():
    if not 'uid' in session:
        return redirect('/')

    if not Music.validate(request.form):
        return redirect('/new_music')

    data = {
        **request.form,
        'user_id': session['uid']
    }

    Music.create(data)

    return redirect('/dashboard')


@app.route('/edit_music/<int:id>')
def edit_music(id):
    if not 'uid' in session:
        return redirect('/')

    data = {
        'id': id,
    }

    music = Music.get_by_id(data)

    return render_template('edit_music.html', music=music)


@app.route('/change_music', methods=["POST"])
def change_music():

    if not Music.validate(request.form):
        return redirect(f'/edit_music/{request.form["id"]}')

    Music.update(request.form)
    return redirect(f'/details/{request.form["id"]}')


@app.route('/details/<int:id>')
def details(id):
    if not 'uid' in session:
        return redirect('/')

    data = {
        'id': id,
    }

    found_music = Music.get_by_id(data)
    user_data = {
        'id': found_music.user_id,
    }

    found_user = User.find_by_id(user_data)

    found_music.creator = found_user

    return render_template('details.html', music=found_music)


@app.route('/delete/<int:id>')
def delete(id):
    if not 'uid' in session:
        return redirect('/')

    data = {
        "id": id
    }
    Music.delete(data)
    return redirect('/dashboard')
