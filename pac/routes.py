from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_required, logout_user, login_user
from pac import db, app, oauth
from pac.models import Note, user_ac
from sqlalchemy import exc


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/notes', methods=['POST', 'GET'])
@login_required
def notes():
    notes = Note.query.order_by(Note.date.desc()).all()
    return render_template('notes.html', notes=notes)


@app.route('/note/<id>')
@login_required
def noteDetail(id):
    note = Note.query.get(id)
    return render_template("noteDetail.html", note=note)


@app.route('/note/<id>/update', methods=['POST', 'GET'])
@login_required
def update(id):
    note = Note.query.get(id)
    if request.method == 'POST':
        note.title = request.form.get('title')
        note.intro = request.form.get('intro')
        note.text = request.form.get('text')
        try:
            db.session.commit()
            return redirect(url_for('notes'))
        except exc.SQLAlchemyError:
            return 'Updating error'
    else:
        return render_template('noteUpdate.html', note=note)


@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        intro = request.form.get('intro')
        text = request.form.get('text')
        notes = Note(title=title, intro=intro, text=text)
        try:
            db.session.add(notes)
            db.session.commit()
            return redirect(url_for('notes'))
        except exc.SQLAlchemyError:
            return 'Database error'
    else:
        return render_template('create.html')


@app.route('/note/<id>/delete')
@login_required
def delete(id):
    note = Note.query.get_or_404(id)
    try:
        db.session.delete(note)
        db.session.commit()
        return redirect(url_for('notes'))
    except exc.SQLAlchemyError:
        return 'An error occured whele deleting the note'


@app.route('/registration', methods=['POST', 'GET'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    if request.method == 'POST':
        if not (login or password or password2):
            flash('Fill all the fields')
        elif password != password2:
            flash('Сheck the correctness of the entered data.')
        else:
            hash_pwd = generate_password_hash(password)
            user_new = user_ac(login=login, password=hash_pwd)
            try:
                db.session.add(user_new)
                db.session.commit()
                return redirect(url_for('login'))
            except exc.SQLAlchemyError:
                return 'An error occured while creating the account'
    else:
        return render_template('register.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        if login and password:
            user = user_ac.query.filter_by(login=login).first()

            if user and check_password_hash(user.password, password):
                login_user(user)
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                else:
                    return redirect(url_for('main'))
            else:
                flash('login or password is not correct')
        else:
            flash('Please fill login and password fields')
    else:
        return render_template('login.html')


@app.route('/loginoauth')
def loginoauth():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # noqa
    # Access token from google (needed to get user info)
    resp = google.get('userinfo')
    user_info = resp.json()
    print(dict(user_info)['id'])
    user = oauth.google.userinfo()  # noqa
    # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got
    # and query your database find/register the user
    # and set ur own data in the session not the profile from google
    login = dict(user_info)['id']
    password = generate_password_hash(dict(user_info)['id'])
    new_user = user_ac(login=login, password=password)
    if user_ac.query.filter_by(login=login).first():

        login_user(user_ac.query.filter_by(login=login).first())
    else:
        try:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
        except exc.SQLAlchemyError:
            return 'An error occured'

    return redirect('/')


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('main'))


@app.after_request
def redirect_to(response):
    if response.status_code == 401:
        return redirect(url_for('login') + '?next=' + request.url)
    else:
        return response
