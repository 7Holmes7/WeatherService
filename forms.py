from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    city = StringField('Город', validators=[DataRequired()])
    submit = SubmitField('Узнать погоду')
