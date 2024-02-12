from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField
from wtforms.validators import DataRequired, Length
from wtforms.widgets.core import TextArea


class addPostForm(FlaskForm):
    namePost = StringField("Название статьи: ", validators=[DataRequired(), Length(min=5, max=20)])
    urlPost = StringField("URL статьи: ", validators=[DataRequired()])
    bodyPost = StringField('Tекст статьи :', widget=TextArea(), validators=[DataRequired(), Length(min=10)])