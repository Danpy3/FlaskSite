from flask_wtf import FlaskForm

from wtforms.fields.simple import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.widgets.core import TextArea


class LoginForm(FlaskForm):
    email = StringField("Email address: ", validators=[Email("Некорректный email")])  # StringField - поле ввода
    psw = PasswordField("Password: ", validators=[DataRequired(), Length(min=4, max=50, message="Пароль должен быть от 4 до 50 символов")])#DataRequired - хотя бы один символ
    remember = BooleanField("Запомнить: ", default=False)
    submit = SubmitField("Войти")


class RegisterForm(FlaskForm):
    name = StringField("Имя: ", validators=[Length(min=4, max=50, message="Имя должно быть от 4 до 50 символов")])
    email = StringField("Email: ", validators=[Email("Некорректный email")])
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100, message="Пароль должен быть от 4 до 100 символов")])

    psw2 = PasswordField("Повтор пароля: ", validators=[DataRequired(), EqualTo('psw', message="Пароли не совпадают")])
    submit = SubmitField("Регистрация")


class FeedbackForm(FlaskForm):
    url = StringField("Url : ", render_kw={'style': 'width: 250px;'})
    BodyMessage = StringField('Сообщение :', widget=TextArea(), validators=[DataRequired(), Length(min=10)])
    submit = SubmitField("Отправить ")