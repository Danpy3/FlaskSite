import sqlite3

from flask import Blueprint, render_template, url_for, redirect, request, flash, session, g
from .admin_forms import addPostForm
from .adminFDataBase import AdminFDataBase

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')


def login_admin():
    session['admin_logged'] = 1


def isLogged():
    return True if session.get('admin_logged') else False


def logout_admin():
    session.pop('admin_logged', None)


menu = [{'url': '.index', 'title': 'Панель'},
        {'url': '.addPost', 'title': 'Добавить статью'},
        {'url': '.listpubs', 'title': 'Список статей'},
        {'url': '.listusers', 'title': 'Список пользователей'},
        {'url': '.logout', 'title': 'Выйти'},
        ]

db = None


@admin.before_request
def before_request():
    global db
    db = g.get('link_db')


@admin.teardown_request
def teardown_request(request):
    global db
    db = None
    return request


@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))

    return render_template('admin/index.html', menu=menu, title='Админ-панель')


@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for(".index"))

    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "12345":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Неверная пара логин/пароль", "error")

    return render_template('admin/login.html', title='Админ-панель')


@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))

    logout_admin()

    return redirect(url_for('.login'))


@admin.route("/add_post", methods=['POST', 'GET'])
def addPost():
    if not isLogged():
        return redirect(url_for('.login'))

    form = addPostForm()

    if db:
        if form.validate_on_submit():
            res = AdminFDataBase(db).addPost(form.namePost.data, form.bodyPost.data, form.urlPost.data)
            if res:
                flash("Статья добавлеDDDDна", category='success')
            else:
                flash("Ошибка добавления", category= 'error')

    return render_template('admin/add_post.html', title='Добавление статьи', menu=menu, form=form)


@admin.route('/list-pubs')
def listpubs():
    if not isLogged():
        return redirect(url_for('.login'))

    lst = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT title, text, url FROM posts")
            lst = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка при получении статей из БД " + str(e))

    return render_template('admin/listpubs.html', title = "Список статей", menu=menu, lst=lst)


@admin.route('/list-users')
def listusers():
    if not isLogged():
        return redirect(url_for('.login'))

    lst = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name, email FROM users ORDER BY time DESC")
            lst = cur.fetchall()
        except sqlite3.Error as e:
            print("Ошибка при получении статей из БД " + str(e))

    return render_template('admin/listusers.html', title = "Список пользователей", menu=menu, lst=lst)