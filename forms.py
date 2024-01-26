from flask_wtf import FlaskForm

from wtforms.fields.simple import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.widgets.core import TextArea


class LoginForm(FlaskForm):
    email = StringField("Email: ", validators=[Email("Некорректный email")])  # StringField - поле ввода
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")])#DataRequired - хотя бы один символ
    remember = BooleanField("Запомнить: ", default=False)
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    name = StringField("Имя: ", validators=[Length(min=4, max=100, message="Имя должно быть от 4 до 100 символов")])
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")])

    psw2 = PasswordField("Повтор пароля: ", validators=[DataRequired(), EqualTo('psw', message="Пароли не совпадают")])
    submit = SubmitField("Регистрация")


class addPostForm(FlaskForm):
    namePost = StringField("Название статьи: ", validators=[DataRequired(), Length(min=5, max=20)])
    urlPost = StringField("URL статьи: ", validators=[DataRequired()])
    bodyPost = StringField('Tекст статьи :', widget=TextArea(), validators=[DataRequired(), Length(min=10, max=200)])
