import sqlite3
import os
from flask import Flask, render_template, request, flash, session, redirect, url_for, abort, g
from FDataBase import FDataBase

# config
DATABASE = "/tmp/flsite.db"
DEBUG = True
SECRET_KEY = 'fdgfh78@#5?>gfhf89dx,v06k'

app = Flask(__name__)
app.config.from_object(__name__)  # инициализация конфигурации приложения

# переопределим путь к базе данных
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'flsite.db')))


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    '''Вспомогаательная функця для создания таблиц БД'''
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
        db.commit()
        db.close()


def get_db():
    '''Соединение с БДБ если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    return render_template('index.html', menu=dbase.getMenu(), posts=dbase.getPostsAnnonce())


@app.route("/add_post", methods=['POST', 'GET'])
def addPost():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['name']) > 4 and len(request.form['post']) > 10:
            res = dbase.addPost(request.form['name'], request.form['post'], request.form['url'])
            if not res:
                flash('Ошибка добавления статьи', category='error')
            else:
                flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('add_post.html', menu=dbase.getMenu(), title='Добавление статьи')


@app.route("/post/<alias>")
def showPost(alias):
    db = get_db()
    dbase = FDataBase(db)
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)

    return render_template('post.html', title=title, menu=dbase.getMenu(), post=post)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    db = get_db()
    dbase = FDataBase(db)
    if request.method == 'POST':
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
    return render_template('contacts.html', title='Our contacts', menu=dbase.getMenu())


@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    return f"Пользователь: {username}"


@app.route('/login', methods=['POST', 'GET'])
def login():
    db = get_db()
    dbase = FDataBase(db)

    if 'userLogged' in session:
        return redirect(url_for('index', username=session['userLogged']))
    elif request.method == 'POST' and request.form['username'] == "selfedu" and request.form['psw'] == "123":
        session['userLogged'] = request.form['username']
        return redirect(url_for('index', username=session['userLogged']))

    return render_template('login.html', title="Авторизация", menu=dbase.getMenu())


@app.errorhandler(404)
def pageNotFount(error):
    return render_template('page404.html', title="Страница не найдена")


@app.errorhandler(401)
def pageNotFount(error):
    return render_template('page401.html', title="Страница не найдена")


if __name__ == "__main__":
    app.run(debug=True)
